<h1 align="center">
    <img src="/static/README/homepage.png">
</h1>

<h4 align="center">
    KnowShows is a web application that makes searching for concert events a better experience
</h4>

<h1 align="center">
    <img src="/static/README/event.gif">
</h1>

<h1 align="center">
    <img src="/static/README/artist.gif">
</h1>

<p align="center">
    <img src="/static/README/python-original-wordmark.png" width="70px"/>
    <img src="/static/README/flask.png" width="70px"/>
    <img src="/static/README/sqlalchemy.jpg" width="70px"/>
    <img src="/static/README/postgresql-original-wordmark.png" width="70px"/>
    <img src="/static/README/ajax.png" width="70px"/>
    <img src="/static/README/logo-json.png" width="70px"/>
    <img src="/static/README/jquery-original-wordmark.png" width="70px"/>
    <img src="/static/README/jinja2.png" width="70px"/>
    <img src="/static/README/html5-css-javascript-logos.png" width="70px"/>
    <img src="/static/README/bootstrap-plain-wordmark.png" width="70px"/>
</p>

<div align="center">
  <h4>
    <a href="#overview">Overview</a> |
    <a href="#features">Features</a> |
    <a href="#requirements">Requirements</a> |
    <a href="#installation">Installation</a> |
    <a href="#futurefeature">Future Feature</a> |
  </h4>
</div>

<a name="overview"/></a>
## Overview
Have you ever looked up a concert lineup and said to yourself, “I don’t know who these bands are” and then went on to google each of them? Or say you’d like to get tickets for you and a friend who loves the Avett Brothers (nudge-nudge, that friend is me) but you’re not familiar with the music of the Avett Brothers.
KnowShows will do the research for you!

<a name="features"/></a>
## Features
- Search by artist name, event name/genre, or venue name
- Optional filters for city/state and date range
- Option to have Google Maps find user's current location and populate city/state fields for user
- Links to share page through Facebook or Twitter
- Provides for each artist:
	- bio summary
	- Spotify playlist with top tracks
	- link to artist's Spotify page
	- link to YouTube search results of the artist
	- list of events for the artist
- Provides for each event:
	- event information
    - link to SeakGeek for event tickets
	- information on each artist in lineup
	- Spotify playlist with each artist's top tracks
- Provides list of events for a venue

<a name="requirements"/></a>
## Requirements

* Obtain API keys from the following APIs and save in secrets.sh file:
    - Spotify (https://developer.spotify.com/dashboard/applications)
    - SeatGeek (https://platform.seatgeek.com/)
    - Google Maps Geocoding and Maps Embed (https://developers.google.com/maps/documentation/)
    - Last.FM (https://www.last.fm/api)

<a name="installation"/></a>
## Installation
```
$ git clone https://github.com/a-ge/HBproject-KnowShows.git
```
Create a virtual environment in the directory:
```
$ virtualenv env
```
Activate virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
$ pip install -r requirements.txt
```
Create .gitignore file:
```
$ touch .gitignore
```
Access .gitignore file in terminal to ignore secrets.sh file:
```
$ nano .gitignore
```
Store secrets.sh file in .gitignore file:
```
secrets.sh
```
Activate secrets.sh:
```
$ source secrets.sh
```
Create database:
```
$ createdb concerts
```
Insert model:
```
$ python3 -i model.py
>>> db.create_all()
```
Run the app:
```
$ python3 server.py
```
Open localhost:5000 on browser.


<a name="futurefeature"/></a>
## Future Feature
* Include other music event APIs like Eventful or Eventbrite