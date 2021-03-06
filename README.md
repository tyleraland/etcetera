etcetera
========

Goal: Collect data from multiple channels and aggregate into a database

Setup
=======
1. Create a virtualenv.

    ```
    $ ./bin/bootstrap.sh
    ```

2. Activate the virtualenv.  All subsequent commands are run with the virtualenv activated

    ```
    $ source etcetera-env/bin/activate
    ```

3. Install the dependencies.  

    ```
    $ pip install -r requirements.txt
    ```

4. Authenticate Google Drive (This can't be automated).  This will give you a URL to paste into your browser and request a verification code.  If successful, the python script will download a credentials file which the google drive API will use to access your account

    ```
    $ ./bin/authenticate_google_drive.py
    ```


Roadmap
=======

*   ~~Implement a Twitter feed using Twitter API~~
    *   Write a utility to insert Twitter archive (like from Twitter.com) into database
*   ~~Fitbit feed using python-fitbit api~~
    *   ~~Request and receive Partner API access~~
*   ~~Build a SMS feed (data on Google Drive a la IFTTT)~~
*   ~~Build Rescuetime feed using their python api~~
*   ~~GPS data, logged with GPSLogger for android and backed up to Google Drive~~
*   ~~Phone call (metadata) logs on Google Drive a la IFTTT~~
*   ~~Last.fm data~~
*   Build Mint feed using mintapi (available via pip!)
*   Build Evernote feed using Evernote SDK (sqlite max string size is 1GB)
*   Email archives / backups.
*   Google Calendar data using API (https://developers.google.com/google-apps/calendar/)
    *   This will also require some tidying up of my calendars so they reflect things I really do
* Script to authenticate the various services
*   ...
*   ...
*   A website to display visualizations (another project)

Inspiration
=======
Brian Staats:
- https://github.com/bstaats/livestaats/tree/e70c9c17b07577aa97610955313b30f0d638f98c
Nicholas Felton
- http://bits.blogs.nytimes.com/2014/08/19/a-life-in-data-nicholas-feltons-self-surveillance/
- http://theofficeof.feltron.com/
Aprilzero
- http://aprilzero.com/
Fitbit
- http://www.jamierubin.net/2013/03/20/one-full-year-of-fitbit-pedometer-data-part-1-a-look-back/
Every day of my life
- http://marcinignac.com/projects/everyday-of-my-life/
The personal analytics of (Stephen Wolfram's) life
- http://blog.stephenwolfram.com/2012/03/the-personal-analytics-of-my-life/
