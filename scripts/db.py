import sqlite3
import os
from os import path

def dbcreate(conf):
    dbpath = conf['database']
    dbpath = dbpath.replace('~', os.environ['HOME'])

    if not path.exists(path.dirname(dbpath)):
        os.makedirs(path.dirname(conf['database']))

    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    tables = [
    """
    CREATE table if not exists
    twitter(datetime TEXT,
            message TEXT,
            UNIQUE(datetime, message)
          on conflict replace);
    """,
    """
    CREATE table if not exists
    sms_sent(datetime TEXT,
             phone_number TEXT,
             contact_name TEXT,
             message TEXT,
             UNIQUE(datetime, message)
       on conflict replace);
    """,
    """
    CREATE table if not exists
    sms_received(datetime TEXT,
                 phone_number TEXT,
                 contact_name TEXT,
                 message TEXT,
                 UNIQUE(datetime, message)
       on conflict replace);
    """,
    """
    CREATE table if not exists
    outgoing_calls(datetime TEXT,
                   phone_number TEXT,
                   contact_name TEXT,
                   duration_seconds INTEGER,
                   UNIQUE(datetime)
       on conflict replace);
    """,
    """
    CREATE table if not exists
    received_calls(datetime TEXT,
                   phone_number TEXT,
                   contact_name TEXT,
                   duration_seconds INTEGER,
                   UNIQUE(datetime)
       on conflict replace);
    """,
    """
    CREATE table if not exists
    missed_calls(datetime TEXT,
                 phone_number TEXT,
                 contact_name TEXT,
                 UNIQUE(datetime)
       on conflict replace);
    """,
    """
    CREATE table if not exists
    fitbit_intraday_steps(datetime TEXT UNIQUE,
                          steps INTEGER,
                          UNIQUE(datetime)
                        on conflict replace);
    """,
    """
    CREATE table if not exists
    rescuetime(datetime TEXT,
               seconds_spent INTEGER,
               activity TEXT,
               category TEXT,
               productivity_score INTEGER);
    """,
    """
    CREATE table if not exists
    last_fm(datetime TEXT,
            artist TEXT,
            track TEXT,
            album TEXT,
            url TEXT);
    """,
    """
    CREATE table if not exists
    gps(datetime TEXT,
        latitude REAL,
        longitude REAL,
        UNIQUE(datetime));
    """]
    for statement in tables:
        cur.execute(statement)
    con.commit()

def dbinsert(conf, table, rows):

    dbpath = conf['database']
    dbpath = dbpath.replace('~', os.environ['HOME'])

    con = sqlite3.connect(dbpath)
    cur = con.cursor()

    con.text_factory = str
    for row in rows:
        # We want to use sqlite's facilities to build our statement string, but that
        # requires knowing how many fields our inserted string will have.  We perform
        # an initial string formatting to insert the proper number of variables
        statement = "insert or replace into {} values ({})".format(
            table, ','.join(['?' for field in row])
        )
        cur.execute(statement, row)
    con.commit()
