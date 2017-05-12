# Swiss Tournament Code
This project is connected to RDB course. And using Vagrant and Virtual Box, 
but can be use any environment which installed with PostgreSQL and Python. 

This sample project was designed to study how to create and use databases and 
how to manipulate the data of tables with python code.

# File Description
    1. tournament.sql       : Table definistions for the tournament project.
    2. tournament.py        : Implementation of a Swiss-system tournament.
    3. tournament_test.py   : Test cases for tournament.py

# Run Procedure
    1. create Database & Table
      1) connect to postgresql with psql command line interface(CLI)
      2) import tournament.sql in psql to create db & table : \i tournament.sql
    2. run test python code 
      1) open bash console : python tournament_test.py


