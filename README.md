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

4. Authenticate Google Drive (This can't be automated)

    ```
    $ ./bin/authenticate_google_drive.py
    ```


Roadmap
=======

1. Implement a Twitter feed, ironically using Google Drive SDK to pull IFTTT data
 . Put data into sqlite database; don't duplicate data
3. Copy the above and build a Fitbit feed (data also stored on Google Drive)
4. Copy the above and build a Sleep feed (Sleep as Android data on Google Drive)
4. Build Evernote feed using Evernote SDK (sqlite max string size is 1GB)
5. Build Mint feed using mintapi (available via pip!)
6. Build Rescuetime feed using their python api 

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
