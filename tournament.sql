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


CREATE TABLE tb_player (
	pid serial primary key,
	pname varchar(100)
	-- won numeric default 0,
	-- lost numeric default 0
);

CREATE TABLE tb_match (
	pid integer primary key,
	won numeric default 0,
	lost numeric default 0
);