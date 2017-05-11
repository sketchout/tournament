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
    QUERY_MATCH = """DELETE FROM matches;"""
    QUERYS_STANDING = """UPDATE standings set wins=0,matches=0;"""
    conn = None
    rows_deleted = 0
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY_MATCH)
        c.execute(QUERYS_STANDING)
        rows_deleted = c.rowcount
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def deletePlayers():
    """Remove all the player records from the database."""
    QUERYS_STANDING = """DELETE FROM standings;"""
    QUERY_PLAYER = """DELETE FROM players;"""
    conn = None
    rows_deleted = 0
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERYS_STANDING)
        c.execute(QUERY_PLAYER)
        rows_deleted = c.rowcount
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted


def countPlayers():
    """Returns the number of players currently registered."""
    QUERY = """SELECT count(pid) FROM players;"""
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        cnt = c.fetchone()[0]
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
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
    QUERY_PLAYER = """
            INSERT INTO players(pname)
            VALUES(%s) returning pid;
            """
    QUERYS_STANDING = """
            INSERT INTO standings(pid,pname,wins,matches)
            VALUES(%s,%s,%s,%s);
            """
    conn = None
    pid = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY_PLAYER, (name,))
        pid = c.fetchone()[0]
        c.execute(QUERYS_STANDING, (pid,name,0,0,))
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return pid


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # QUERY = """
    #     select a.pid, a.pname, b.won as wins, b.won+b.lost as matches
    #     from tb_player a
    #     left join tb_match b
    #         on a.pid = b.pid
    #     order by b.won desc;
    #     """
    QUERY = """
        SELECT pid, pname, wins, matches FROM standings
        ORDER by wins DESC
    """
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rs = c.fetchall()
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
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
    QUERY_MATCH = """INSERT INTO matches(winner,loser)
                VALUES(%s, %s);"""
    QUERYS_WIN = """UPDATE standings
                SET wins=wins+1, matches=matches+1
                WHERE pid=(%s);"""
    QUERYS_LOSS = """UPDATE standings
                SET matches=matches+1
                WHERE pid=(%s);"""
    conn = None
    mid = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY_MATCH, (winner,loser,))
        c.execute(QUERYS_WIN, (winner,))
        c.execute(QUERYS_LOSS, (loser,))
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


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
        SELECT a.pid as id1, a.pname as name1, b.pid as id2, b.pname as name2
        FROM ( SELECT row_number() over(ORDER BY wins desc)+1 as rank ,
                pid, pname FROM standings ORDER BY wins) a
        LEFT JOIN ( SELECT row_number() over(ORDER BY wins desc) as rank,
                pid, pname FROM standings ORDER BY wins ) b
            on a.rank = b.rank
        WHERE mod(a.rank, 2) = 0
        ORDER BY a.rank;
        """
    conn = None
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(QUERY)
        rs = c.fetchall()
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rs
