CREATE TABLE teams(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    games INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    loses INTEGER NOT NULL,
    points INTEGER NOT NULL,
    gdifference INTEGER NOT NULL
);

CREATE TABLE players(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    team_id INTEGER NOT NULL,
    birth_year INTEGER NOT NULL,
    country VARCHAR(50),
    birth_place VARCHAR(50),
    height INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    shoots VARCHAR(10),
    points INTEGER NOT NULL,
    goals INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    number INTEGER NOT NULL,
    games INTEGER NOT NULL,
    plusminus INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    mail VARCHAR(80) NOT NULL,
    birth_year INTEGER NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    type INTEGER NOT NULL
);

CREATE TABLE favplayers(
    id SERIAL PRIMARY KEY NOT NULL,
    usr_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES users(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE favteams(
    id SERIAL PRIMARY KEY NOT NULL,
    usr_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES users(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE FUNCTION trigger_players_before_del () RETURNS trigger AS '
BEGIN
while (select count(*) from favplayers where favplayers.player_id = OLD.id)>0
loop
if (select count(*) from favplayers where favplayers.player_id = OLD.id)>0
then delete from favplayers where favplayers.player_id = OLD.id;
end if;
end loop;
return OLD;
END;
' LANGUAGE  plpgsql;

CREATE TRIGGER tr_player_del_befor
BEFORE DELETE ON players FOR EACH ROW
EXECUTE PROCEDURE trigger_players_before_del();

CREATE FUNCTION trigger_teams_before_del () RETURNS trigger AS '
BEGIN
while (select count(*) from favteams where favteams.team_id = OLD.id)>0
loop
if (select count(*) from favteams where favteams.team_id = OLD.id)>0
then delete from favteams where favteams.team_id = OLD.id;
end if;
end loop;
while (select count(*) from players where players.team_id = OLD.id)>0
loop
if (select count(*) from players where players.team_id = OLD.id)>0
then delete from players where players.team_id = OLD.id;
end if;
end loop;
return OLD;
END;
' LANGUAGE  plpgsql;

CREATE TRIGGER tr_team_del_befor
BEFORE DELETE ON teams FOR EACH ROW
EXECUTE PROCEDURE trigger_teams_before_del();

CREATE FUNCTION trigger_users_before_del () RETURNS trigger AS '
BEGIN
while (select count(*) from favplayers where favplayers.usr_id = OLD.id)>0
loop
if (select count(*) from favplayers where favplayers.usr_id = OLD.id)>0
then delete from favplayers where favplayers.usr_id = OLD.id;
end if;
end loop;
while (select count(*) from favteams where favteams.usr_id = OLD.id)>0
loop
if (select count(*) from favteams where favteams.usr_id = OLD.id)>0
then delete from favteams where favteams.usr_id = OLD.id;
end if;
end loop;
return OLD;
END;
' LANGUAGE  plpgsql;

CREATE TRIGGER tr_user_del_befor
BEFORE DELETE ON users FOR EACH ROW
EXECUTE PROCEDURE trigger_users_before_del();

CREATE USER simple_user password 'user';
GRANT SELECT ON players TO simple_user;
GRANT SELECT ON teams TO simple_user;
GRANT SELECT, DELETE ON favteams TO simple_user;
GRANT SELECT, DELETE ON favplayers TO simple_user;

CREATE USER moderator_user password 'moder';
GRANT ALL ON players TO moderator_user;
GRANT ALL ON teams TO moderator_user;
GRANT ALL ON favteams TO moderator_user;
GRANT ALL ON favplayers TO moderator_user;

CREATE USER administrator password 'admn';
GRANT ALL ON players TO administrator;
GRANT ALL ON teams TO administrator;
GRANT ALL ON favteams TO administrator;
GRANT ALL ON favplayers TO administrator;
GRANT ALL ON users TO administrator;