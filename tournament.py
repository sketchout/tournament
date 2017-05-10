#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    QUERY = """update tb_match
                set won=0, lost=0;"""
    conn = None
    rows_deleted = 0
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rows_deleted = c.rowcount
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def deletePlayers():
    """Remove all the player records from the database."""
    QUERY = """delete from tb_player;"""
    conn = None
    rows_deleted = 0
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rows_deleted = c.rowcount
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def countPlayers():
    """Returns the number of players currently registered."""
    QUERY = """select count(*) from tb_player;"""
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        cnt = c.fetchone()[0]
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    QUERY = """insert into tb_player(pname) values(%s) returning id;"""
    conn = None
    pid = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY, (name,))
        pid = c.fetchone()[0]
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return pid


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    QUERY = """
        select a.pid, a.pname, b.won as wins, b.won+b.lost as matches
        from tb_player a, tb_match b
        where a.pid = b.pid
        order by a.won desc;
        """
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rs = c.fetchall()
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rs


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    QUERY_WON = """update tb_match
                set won = won + 1
                where pid = %s;"""
    QUERY_LOST = """update tb_match
                set lost = lost + 1
                where pid = %s;"""

    conn = None
    rows_updated = 0
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY_WON, (winner,))
        c.execute(QUERY_LOST, (loser,))
        row_updated = c.rowcount
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_updated


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    QUERY = """
        select a.id as id1, a.name as name1, b.id as id2, b.name as name2
        from ( select row_number() over(order by won desc)+1 as rank ,
                id, name from tb_player ) a
        left join ( select row_number() over(order by won desc) as rank,
                id, name from tb_player ) b
            on a.rank = b.rank
        where mod(a.rank, 2) = 0
        order by a.rank;
        """
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rs = c.fetchall()
        conn.commit()
        conn.close()
    except( Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rs

