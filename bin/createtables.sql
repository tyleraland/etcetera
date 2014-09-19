CREATE table if not exists Twitter(datetime TEXT UNIQUE, content TEXT);
CREATE table if not exists sms_send(datetime TEXT, timezone TEXT, number TEXT, contact_name TEXT, message TEXT, UNIQUE(datetime, timezone, message) on conflict replace);
CREATE table if not exists sms_recv(datetime TEXT, timezone TEXT, number TEXT, contact_name TEXT, message TEXT, UNIQUE(datetime, timezone, message) on conflict replace);
CREATE table if not exists Fitbit_intraday_steps(datetime TEXT UNIQUE, steps INTEGER);
