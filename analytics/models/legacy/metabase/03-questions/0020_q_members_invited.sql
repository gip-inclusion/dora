-- Question : 
-- liste des membres invités

-- noqa: disable=LT05

drop view if exists q_members_invited;

create view q_members_invited as
select
    "ID utilisateur",
    "Nom",
    "Prénom",
    "E-mail",
    "E-mail validé",
    "Date de création",
    "Dernière connexion",
    "Nom de la structure",
    "URL Dora",
    "SLUG",
    "Département",
    "Date d'invitation",
    "Invitation en tant qu'admin",
    "Compte inactif",
    "Nombre d'admins dans la structure",
    "Premier admin de la structure",
    "Membre d'autres structures"
from mb_putative_members
where "Invitation par un admin";

comment on view q_members_invited is 'Liste des membres invités en attente de rattachement';
