CREATE table if not exists 
Twitter(datetime TEXT UNIQUE, 
        timezone TEXT,
        message TEXT,
        UNIQUE(datetime,timezone,message)
      on conflict replace);

CREATE table if not exists 
sms_send(datetime TEXT, 
         timezone TEXT, 
         phone TEXT, 
         contact_name TEXT, 
         message TEXT, 
         UNIQUE(datetime, timezone, message) 
        on conflict replace);

CREATE table if not exists 
sms_recv(datetime TEXT, 
         timezone TEXT, 
         phone TEXT, 
         contact_name TEXT, 
         message TEXT, 
         UNIQUE(datetime, timezone, message) 
        on conflict replace);

CREATE table if not exists 
Fitbit_intraday_steps(datetime TEXT UNIQUE, 
                      timezone TEXT, 
                      steps INTEGER, 
                      UNIQUE(datetime, timezone) 
                    on conflict replace);
