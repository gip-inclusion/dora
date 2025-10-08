import argparse
import re
from collections import Counter
from urllib.parse import unquote, urlparse

import psycopg2
import sqlglot

MAX_JOINS = 3

QUESTIONS = {}
TABLE_NAMES = {}
TABLE_FIELDS = {}

# 73 = TDB Pilotage département
# 79 = Nouvelle stats public 2023
# 86 = Gestion des structures ADIE
# 90 = Suivi du remplacement de la fiche de liaison - Drôme
# 92 = Objectifs 03.24 > 09.24
# 100 = Suivi du remplacement de la fiche de liaison CD
# question 447 = Liste des gestionnaires
# question 863 = Tableau de bord biz dev MVP v4


def _first_item(cur):
    return [row[0] for row in cur.fetchall()]


def get_question_ids(cur, dashboard_id):
    cur.execute(
        """
        select distinct(card_id)
        from report_dashboardcard
        where dashboard_id = %s
    """,
        (dashboard_id,),
    )
    return _first_item(cur)


def fix_metabase_syntax(query):
    def replace_model_syntax(match):
        placeholder = match.group(1).strip()
        return f'(SELECT * FROM "{placeholder}")'

    query = re.sub(r"\[\[.*?\]\]", "", query)  # Metabase optional snippets
    return re.sub(r"{{([^}]+)}}", replace_model_syntax, query)


def extract_field_ids(lst):
    """Given a Metabase filter query like:
        ['and', ['=', ['field', 267, None], True], ['!=', ['field', 263, None], 'PE']]
    returns a list of field IDs: [267, 263]
    """
    result = []
    if isinstance(lst, list):
        if len(lst) >= 3 and lst[0] == "field":
            result.append(lst[1])  # Append the ID (second element)
        for item in lst:
            result.extend(extract_field_ids(item))
    return result


class MetabaseQuestion:
    def __init__(self, id, query):
        self.id = id
        self.type = query["type"]
        self.database = query["database"]
        self.source_table = None
        self.query = None
        self.joins = []
        self.filters = []
        self.inception_level = 0
        if self.type == "native":
            self.query = fix_metabase_syntax(query["native"]["query"])
            parsed = sqlglot.parse_one(self.query)
            ctes = [cte.alias for cte in parsed.find_all(sqlglot.exp.CTE)]
            for table in parsed.find_all(sqlglot.exp.Table):
                if table.name not in ctes and not table.alias:
                    # first found table is considered the "source" table
                    if not self.source_table:
                        self.source_table = table.name
                    else:
                        self.joins.append(table.name)
        else:
            query = query["query"]
            # not clear why. example: https://metabase.dora.inclusion.beta.gouv.fr/question/612
            while "source-query" in query:
                query = query["source-query"]
            self.source_table = query["source-table"]
            if "filter" in query:
                self.filters = [
                    TABLE_FIELDS.get(id, id)
                    for id in extract_field_ids(query["filter"])
                ]
            if "joins" in query:
                self.joins = [join["source-table"] for join in query["joins"]]

    def resolve_inceptions(self):
        if isinstance(self.source_table, str) and self.source_table.startswith(
            "card__"
        ):
            src_question_id = int(self.source_table.removeprefix("card__"))
            src_question = QUESTIONS[src_question_id]
            self.source_table = src_question.source_table
            self.joins += src_question.joins
            self.inception_level += 1 + len(src_question.joins)

        all_joins = []
        for join in self.joins:
            if isinstance(join, str) and join.startswith("card__"):
                src_question_id = int(join.removeprefix("card__"))
                src_question = QUESTIONS[src_question_id]
                self.inception_level += 1 + len(src_question.joins)
                all_joins.append(src_question.source_table)
                all_joins += src_question.joins
            else:
                all_joins.append(join)
        self.joins = all_joins

    def resolve_names(self):
        self.joins = [TABLE_NAMES.get(join, join) for join in self.joins]
        self.source_table = TABLE_NAMES.get(self.source_table, self.source_table)


def main():
    parser = argparse.ArgumentParser(description="Metabase dashboard analyzer")
    parser.add_argument(
        "connection_url", type=str, help="Metabase internal DB connection URL"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Tunnel host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=10000, help="Tunnel port (default: 10000)"
    )
    parser.add_argument(
        "--dashboard-ids",
        nargs="+",
        type=int,
        default=[],
        help="Space-separated numeric IDs of dashboards",
    )
    parser.add_argument(
        "--question-ids",
        nargs="+",
        type=int,
        default=[],
        help="Space-separated numeric IDs of questions",
    )

    args = parser.parse_args()

    parsed_url = urlparse(args.connection_url)
    conn_params = {
        "host": args.host,
        "port": args.port,
        "dbname": parsed_url.path.lstrip("/"),
        "user": unquote(parsed_url.username),
        "password": unquote(parsed_url.password),
    }

    con = psycopg2.connect(**conn_params)
    cur = con.cursor()

    dashboards = {}

    for dashboard_id in args.dashboard_ids:
        question_ids = get_question_ids(cur, dashboard_id)
        # some cards in a dashboard a re not a question
        dashboards[dashboard_id] = [q for q in question_ids if q is not None]

    cur.execute("select id, name from metabase_table")
    for id, name in cur.fetchall():
        TABLE_NAMES[id] = name

    cur.execute("select id, name from metabase_field")
    for id, name in cur.fetchall():
        TABLE_FIELDS[id] = name

    cur.execute(
        "select id, dataset_query::jsonb "
        "from report_card where not archived order by id"
    )
    for card_id, query in cur.fetchall():
        QUESTIONS[card_id] = MetabaseQuestion(card_id, query)

    for question in QUESTIONS.values():
        try:
            question.resolve_inceptions()
        except KeyError:
            print(
                f"Could not resolve inceptions for question {question.id},"
                " source question does not exist"
            )
            continue
        question.resolve_names()

    all_questions = set()
    for dashboard_id, question_ids in dashboards.items():
        all_questions.update(question_ids)
        print(f"############### analyse dashboard={dashboard_id}")
        print("nb questions:", len(question_ids))
        all_tables = set()
        print("> questions utilisées")
        for question_id in sorted(question_ids):
            q = QUESTIONS[question_id]
            print(f"\t{q.id=} {q.source_table=} {q.inception_level=}")
            for join in q.joins:
                print(f"\t\tJOIN on {join}")
            all_tables.add(q.source_table)
            all_tables.update(q.joins)
        print("> tables référencées")
        for table in sorted([t for t in all_tables if t]):
            print(f"\t{table}")

    for question_id in args.question_ids:
        print(f"############### analyse question={question_id}")
        all_questions.add(question_id)
        q = QUESTIONS[question_id]
        print(f"\t{q.id=} {q.source_table=} {q.inception_level=}")
        for join in q.joins:
            print(f"\t\tJOIN on {join}")
        for filter in q.filters:
            print(f"\t\tFILTER on {filter}")

    table_occurrences = Counter()
    join_pairs = []
    for q_id in all_questions:
        question = QUESTIONS[q_id]
        for i in range(len(question.joins)):
            for j in range(i + 1, len(question.joins)):
                if question.joins[i] != question.joins[j]:
                    pair = tuple(sorted((question.joins[i], question.joins[j])))
                    join_pairs.append(pair)
        table_occurrences[question.source_table] += 1
        for join in question.joins:
            if question.source_table != join:
                table_occurrences[join] += 1
                pair = tuple(sorted((question.source_table, join)))
                join_pairs.append(pair)

    print("############### top tables")
    for table, count in sorted(
        dict(table_occurrences).items(), key=lambda x: x[1], reverse=True
    ):
        print(f"{table}: {count} occurrences")

    print("############### top joins")
    pair_frequencies = Counter(join_pairs)
    most_joined = sorted(pair_frequencies.items(), key=lambda x: x[1], reverse=True)
    for pair, freq in most_joined:
        print(f"{pair[0]} - {pair[1]}: {freq}")

    cur.close()
    con.close()


if __name__ == "__main__":
    main()
