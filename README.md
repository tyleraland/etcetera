ghosteye
========

Goal: Collect data from multiple channels and aggregate into a database

Roadmap
=======

1 Implement a Twitter fetcher, ironically using Google Drive SDK to pull IFTTT data
 * Put data into sqlite database; don't duplicate data
3 Copy the above and build a Fitbit fetcher (data also stored on Google Drive)
4 Copy the above and build a Sleep fetcher (Sleep as Android data on Google Drive)
4 Build Evernote fetcher using Evernote SDK (sqlite max string size is 1GB)
5 Build Mint fetcher using mintapi (available via pip!)
6 Build Rescuetime fetcher using their python api 
...
? GPS data from my android phone
...
Z A website to display visualizations (probably another project)

Inspiration
=======
Brian Staats: 
- https://github.com/bstaats/livestaats/tree/e70c9c17b07577aa97610955313b30f0d638f98c
Nicholas Felton 
- http://bits.blogs.nytimes.com/2014/08/19/a-life-in-data-nicholas-feltons-self-surveillance/
- http://theofficeof.feltron.com/
