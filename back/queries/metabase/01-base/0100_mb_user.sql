drop table if exists mb_user;

create table mb_user as
select
    users_user.id,
    users_user.ic_id,
    users_user.email,
    users_user.last_name,
    users_user.first_name,
    users_user.is_valid,
    users_user.is_staff,
    users_user.is_manager,
    users_user.departments,
    users_user.date_joined,
    users_user.last_login,
    users_user.last_service_reminder_email_sent,
    users_user.newsletter,
    users_user.main_activity,
    (select users_user.departments[1]) as department,
    (
        select users_user.last_service_reminder_email_sent
    )                                  as last_notification_email_sent
--
from users_user
where (users_user.is_active is true);

alter table mb_user add primary key (id);
