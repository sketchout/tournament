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

CREATE TABLE standings (
    sid serial primary key,
    pid integer references players(pid),
    pname text,
    wins integer,
    matches integer
);