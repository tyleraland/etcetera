import sqlite3

def dbcreate(conf):
    con = sqlite3.connect(conf['database'])
    cur = con.cursor()
    tables = [
    """
    CREATE table if not exists 
    Twitter(datetime TEXT,
            message TEXT,
            UNIQUE(datetime, message)
          on conflict replace);
    """,
    """
    CREATE table if not exists 
    sms(datetime TEXT, 
        direction TEXT,
        phone TEXT, 
        contact_name TEXT, 
        message TEXT, 
        UNIQUE(datetime, direction, message) 
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
    gps(datetime TEXT,
        latitude REAL,
        longitude REAL,
        UNIQUE(datetime));
    """]
    for statement in tables:
        cur.execute(statement)
    con.commit()

def dbinsert(conf, table, rows):

    con = sqlite3.connect(conf['database'])
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
