import json
from pathlib import Path

from dora.core.commands import BaseCommand


class Command(BaseCommand):
    help = (
        "Dans le dossier du back, générer un bilan de bandit avec `bandit -r . --exclude ./.venv/ --format json -o security_report.json`"
        "Analyser ce bilan avec ce script avec python manage.py generate_security_report ./security_report.json"
    )

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str)

    def handle(self, *args, **options):
        json_file = options["json_file"]

        self.analyze_security_report(json_file)

    def analyze_security_report(self, json_file):
        try:
            with open(json_file, "r") as f:
                report = json.load(f)
        except FileNotFoundError:
            print(f"Erreur: Fichier '{json_file}' pas trouvé")
            return
        except json.JSONDecodeError:
            print(f"Erreur: JSON invalide à '{json_file}'")
            return

        results = report.get("results", [])

        custom_issues = self.detect_custom_vulnerabilities(json_file)
        results.extend(custom_issues)

        if not results:
            print("✅ AUCUNE VULNÉRABILITÉ DE SECURITÉ DÉTECTÉ")
            return

        critical_issues = []
        high_risk_issues = []

        for result in results:
            test_id = result.get("test_id", "")
            severity = result.get("issue_severity", "").upper()
            confidence = result.get("issue_confidence", "").upper()

            # Only include high-confidence or high-severity issues
            if confidence in ["HIGH", "MEDIUM"] or severity == "HIGH":
                if test_id in self.CRITICAL_ISSUES:
                    critical_issues.append(result)
                elif test_id in self.HIGH_RISK_ISSUES or severity == "HIGH":
                    high_risk_issues.append(result)

        total_actionable = len(critical_issues) + len(high_risk_issues)

        if total_actionable == 0:
            print("✅ AUCUNE VULNÉRABILITÉ DE SECURITÉ ACTIONNABLE DÉTECTÉ")
            return

        print(
            f"🚨 VULNÉRABILITÉS DE SECURITÉ DÉTECTÉES: {total_actionable} problèmes exique de l'attention immédiate\n"
        )

        # Output critical issues first
        if critical_issues:
            print("=" * 60)
            print("🔴 PROBLÈMES DE SÉCURITÉ CRITIQUES (RÉGLER TOUT DE SUITE)")
            print("=" * 60)

            for i, issue in enumerate(critical_issues, 1):
                self.output_issue(issue, i, "CRITIQUE")

        # Output high-risk issues
        if high_risk_issues:
            print("=" * 60)
            print("🟡 PROBLÈMES DE SÉCURITÉ À HAUTE RISQUE")
            print("=" * 60)

            for i, issue in enumerate(high_risk_issues, len(critical_issues) + 1):
                self.output_issue(issue, i, "HIGH")

        # Summary
        print("=" * 60)
        print("📋 Sommaire")
        print("=" * 60)
        if critical_issues:
            print(
                f"🔴 Problèmes critiques : {len(critical_issues)} (RÉGLER TOUT DE SUITE)"
            )
        else:
            print("✅  Aucun problème critique")
        if high_risk_issues:
            print(f"🟡 Problèmes à haute risque : {len(high_risk_issues)}")
        else:
            print("✅ Aucun problème à haute risque")
        print(f"📍 Total nombre de problèmes : {total_actionable}")

    def detect_custom_vulnerabilities(self, json_file):
        # Détecter des problèmes qui n'ont pas été trouvés par Bandit
        custom_issues = []

        base_path = Path(json_file).parent
        if not base_path.exists():
            base_path = Path.cwd()

        mark_safe_issues = self.scan_for_mark_safe(base_path)
        custom_issues.extend(mark_safe_issues)

        return custom_issues

    def scan_for_mark_safe(self, base_path):
        issues = []

        patterns = ["**/*.py"]

        for pattern in patterns:
            for file_path in base_path.glob(pattern):
                if file_path.is_file():
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()

                        for line_num, line in enumerate(lines, 1):
                            line_stripped = line.strip()

                            if (
                                "mark_safe" in line_stripped
                                and self.is_dangerous_mark_safe(line_stripped)
                            ):
                                issue = {
                                    "test_id": "XSS001",
                                    "filename": str(file_path),
                                    "line_number": line_num,
                                    "issue_text": "Potential XSS vulnerability with mark_safe usage",
                                    "issue_severity": "HIGH",
                                    "issue_confidence": "MEDIUM",
                                    "code": line.rstrip(),
                                    "test_name": "django_mark_safe_xss",
                                }
                                issues.append(issue)

                    except (UnicodeDecodeError, PermissionError):
                        continue

        return issues

    @staticmethod
    def is_dangerous_mark_safe(line):
        dangerous_patterns = [
            "request.POST",
            "request.GET",
            "request.data",
            ".format(",
            "% ",
            'f"',
            "f'",
            "user_input",
            "form.cleaned_data",
            ".POST.get",
            ".GET.get",
            "json.loads",
            "request.body",
        ]

        static_patterns = ["'<", '"<', "<strong>", "<em>", "<br>", "<hr>"]

        for pattern in static_patterns:
            if pattern in line:
                return False

        for pattern in dangerous_patterns:
            if pattern in line:
                return True

        return False

    def output_issue(self, issue, number, risk_level):
        test_id = issue.get("test_id", "Inconnu")
        filename = issue.get("filename", "Fichier inconnu")
        line_number = issue.get("line_number", "Ligne inconnue")
        issue_text = issue.get("issue_text", "Pas de déscription")
        severity = issue.get("issue_severity", "Inconnu")
        confidence = issue.get("issue_confidence", "Inconnu")

        try:
            rel_path = str(Path(filename).relative_to(Path.cwd()))
        except ValueError:
            rel_path = filename

        print(f"\n[{number}] {risk_level} - {test_id}")
        print(f"📁 Fichier : {rel_path}")
        print(f"📍 Ligne : {line_number}")
        print(f"⚠️  Problème : {issue_text}")
        print(f"🎯 Sévérité : {severity} | Confiance: {confidence}")

        code = issue.get("code", "").strip()
        if code:
            print("💻 Code :")
            for line in code.split("\n"):
                print(f"    {line}")

        fix_guidance = self.get_fix_guidance(test_id)
        if fix_guidance:
            print(f"🔧 Fix : {fix_guidance}")

    @staticmethod
    def get_fix_guidance(test_id):
        guidance_map = {
            "B608": 'Utilisez des requêtes paramétrées : cursor.execute("SELECT * FROM table WHERE id = %s", [user_id])',
            "B609": "Évitez le formatage de chaînes dans SQL. Utilisez l'ORM de Django ou des requêtes paramétrées.",
            "B610": "Remplacez les chaînes de format par des requêtes paramétrées ou des méthodes de l'ORM de Django.",
            "B611": "Utilisez des requêtes paramétrées au lieu de .format() sur les chaînes SQL.",
            "B703": "Remplacez le SQL brut par l'ORM de Django ou assurez une paramétrisation appropriée.",
            "B105": "Déplacez les mots de passe codés en dur vers des variables d'environnement ou une configuration sécurisée.",
            "B106": "Utilisez des variables d'environnement pour la configuration sensible.",
            "B301": "Remplacez pickle par une sérialisation plus sûre comme JSON.",
            "B501": "Activez la validation des certificats SSL en production.",
            "B506": "Utilisez yaml.safe_load() au lieu de yaml.load().",
            "B307": "Évitez eval(). Utilisez ast.literal_eval() pour une évaluation sûre.",
            "B102": "Supprimez l'utilisation de exec() ou validez soigneusement l'entrée.",
            "B113": "Ajoutez un paramètre de timeout aux requêtes : requests.get(url, timeout=30)",
            "XSS001": 'Utilisez format_html() ou escape() avant mark_safe() : format_html("<strong>{}</strong>", user_input)',
        }

        return guidance_map.get(test_id)

    CRITICAL_ISSUES = {
        "B608": "Hardcoded SQL expression",
        "B609": "SQL Injection via string concatenation",
        "B610": "Potential SQL injection on extra function",
        "B611": "Potential SQL injection on RawSQL function",
        "B703": "Django mark_safe usage",
        "B201": "Flask debug mode is enabled",
        "B501": "SSL/TLS certificate validation disabled",
        "B502": "SSL/TLS insecure cipher usage",
        "B506": "YAML load vulnerability using yaml.load()",
        "B301": "Use of insecure pickle module",
        "B302": "Insecure deserialization",
        "B303": "Use of insecure MD5 hash algorithm",
        "B304": "Use of insecure cipher",
        "B305": "Use of insecure cipher mode",
        "B306": "Insecure temporary file handling",
        "B307": "Use of eval() function",
        "B102": "Use of exec() function",
        "B701": "Jinja2 autoescape disabled",
        "B702": "Use of Mako templates",
    }

    HIGH_RISK_ISSUES = {
        "B104": "Hardcoded bind to all network interfaces",
        "B105": "Hardcoded password in code",
        "B106": "Hardcoded password in function argument",
        "B107": "Hardcoded password as default value",
        "B108": "Hardcoded temporary file directory",
        "B110": "Use of try-except-pass",
        "B112": "Use of try-except-continue",
        "B113": "HTTP request without timeout",
        "B324": "Use of insecure MD5 hash algorithm in hashlib",
        "B325": "Insecure temporary file handling",
        "B401": "Import of insecure telnetlib module",
        "B402": "Import of insecure ftplib module",
        "B403": "Import of insecure pickle module",
        "B404": "Import of subprocess module",
        "B405": "Import of XML libraries",
        "B406": "Import of insecure mktemp module",
        "B407": "Import of XML libraries with XMLParser",
        "B408": "Import of xml.sax module",
        "B409": "Import of xml.dom.minidom module",
        "B410": "Import of lxml module",
        "B411": "Use of random module for cryptographic purposes",
    }
