ghosteye
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
    $ source ghosteye-env/bin/activate
    ```

3. Install the dependencies.  

    ```
    $ pip install -r requirements.txt
    ```

4. Authenticate Google Drive (This can't be automated).  This will give you a URL to paste into your browser and request a verification code.  If successful, the python script will download a .drive_credentials file which the google drive API will use to access your account

    ```
    $ ./bin/authenticate_google_drive.py
    ```


Roadmap
=======

*   Implement a Twitter feed, ironically using Google Drive SDK to pull IFTTT data
    *   Put data into sqlite database; don't duplicate data
*   Copy the above and build a Fitbit feed (data also stored on Google Drive)
*   Copy the above and build a SMS feed (data on Google Drive a la IFTTT)
*   Copy the above and build a Sleep feed (Sleep as Android data on Google Drive)
*   Build Evernote feed using Evernote SDK (sqlite max string size is 1GB)
*   Build Mint feed using mintapi (available via pip!)
*   Build Rescuetime feed using their python api 
*   ...
*   GPS data from my android phone
*   ...
*   A website to display visualizations (probably another project)

Inspiration
=======
Brian Staats: 
- https://github.com/bstaats/livestaats/tree/e70c9c17b07577aa97610955313b30f0d638f98c
Nicholas Felton 
- http://bits.blogs.nytimes.com/2014/08/19/a-life-in-data-nicholas-feltons-self-surveillance/
- http://theofficeof.feltron.com/
