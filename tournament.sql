-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament;


CREATE TABLE players (
	pid serial primary key,
	pname text not null
);

CREATE TABLE matches (
	mid serial primary key,
	winner integer references players(pid),
	loser integer references players(pid)
);

CREATE VIEW view_wins as (
	SELECT players.pid, count(matches.mid) as wins
	FROM players left outer join matches
		on players.pid = matches.winner
	GROUP BY players.pid
);

CREATE VIEW view_played as (
	SELECT players.pid, count(matches.mid) as played
	FROM players left outer join matches
		on players.pid = matches.winner
			or players.pid = matches.loser
	GROUP BY players.pid
);