CREATE table if not exists 
Twitter(datetime TEXT,
        message TEXT,
        UNIQUE(datetime, message)
      on conflict replace);

CREATE table if not exists 
sms(datetime TEXT, 
    direction TEXT,
    phone TEXT, 
    contact_name TEXT, 
    message TEXT, 
    UNIQUE(datetime, direction, message) 
   on conflict replace);

CREATE table if not exists 
fitbit_intraday_steps(datetime TEXT UNIQUE, 
                      steps INTEGER, 
                      UNIQUE(datetime) 
                    on conflict replace);
CREATE table if not exists
rescuetime(datetime TEXT,
           seconds_spent INTEGER,
           activity TEXT,
           category TEXT,
           productivity_score INTEGER);
