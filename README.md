<h1 align="center">
    <img src="/static/README/home.gif">
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
	<!-- Tech Stacks -->
    <img src="https://img.shields.io/npm/v/spaceship-prompt.svg?style=flat-square"/>
<!-- 
**Frontend:** Javascript, AJAX, JSON, jQuery, Jinja, HTML, CSS, Bootstrap</br>
**Backend:** Python, Flask, SQLAlchemy, PostgreSQL<br/>
**APIs:** SeatGeek, Spotify, Google Maps, Last.FM<br/>
-->
</p>

<div align="center">
	<!-- Table of Contents -->
  <h4>
    <a href="#overview">Overview</a> |
    <a href="#features">Features</a> |
    <a href="#requirements">Requirements</a> |
    <a href="#installation">Installation</a> |
    <a href="#features">Future Features</a> |
  </h4>
</div>

<a name="overview"/></a>
## Overview
Have you ever looked up a concert lineup and said to yourself, “I don’t know who these bands are” and then went on to google each of them? Or say you’d like to get tickets for you and a friend who loves the Avett Brothers (nudge-nudge, that friend is me) but you’re not familiar with the music of the Avett Brothers.
KnowShows will do the research for you!

<a name="features"/></a>
## Features
- Search by artist, event, or artist name
- Optional fields for city/state and date range
- Option to have Google Maps find user's current location and populate city/state field for user
- Links to share page through Facebook or Twitter
- Provides for each artist:
	- bio summary
	- Spotify playlist with top tracks
	- link to artist's Spotify page
	- link to YouTube search results of the artist
	- list of events for the artist
- Provides for each event:
	- event information
	- artist information
	- Spotify playlist with each artist's top tracks
- Provides for list of events for a venue

<a name="requirements"/></a>
## Requirements

<a name="installation"/></a>
## Installation
Get Client ID and Key from [Yelp](https://www.yelp.com/fusion) and save them to a file `secrets.sh`:
```
export yelp_client_id="YOUR_CLIENT_ID"
export yelp_api_key="YOUR_KEY"
```
Get Key from [Google Maps](https://cloud.google.com/maps-platform/?apis=maps) and save them to the same file `secrets.sh`:
```
export google_api_key="YOUR_KEY"
``` web application for users to find music concerts and to become familiarized with all the artists in the concert lineup by providing artist information and a Spotify playlist for each of the artists’ top tracks.
On local machine, go to directory where you want to work and clone Discover San Francisco repository:
```
$ git clone https://github.com/jessicahojh/San_Francisco_Webpage_Project.git
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
Create database:
```
$ createdb sanfrancisco
```
Seed data into the database tables:
```
$ python3 seed.py
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
Run the app:
```
$ python3 server.py
```
Open localhost:5000 on browser.

<a name="demo"/></a>
## Demo
**Homepage:**
<br/><br/>
![Homepage](/static/README/homepage.png)
<br/>

**List of Neighborhoods:**
<br/><br/>
![Neighborhoods](/static/README/neighborhoods.gif)
<br/>

**View a specific neighborhood:**
<br/><br/>
![View specific neighborhood](/static/README/specific_neighborhood.png)
<br/>

**View a specific neighborhood's list of "things-to-do/see":**
<br/><br/>
![View list of "things-to-do/see"](/static/README/list_places.gif)
<br/>

**Specific place ("things-to-see") in a specific neighborhood:**
<br/><br/>
![View a specific place in a neighborhood](/static/README/specific_place.gif)
<br/>


**Top 5 Most Popular Restaurants for a specific neighborhood:**
<br/><br/>
![Top 5 Restaurants](/static/README/restaurants.gif)
<br/> 

<a name="features"/></a>
## Future Features
* Using various APIs such as Zillow, weather, and Eventbright to provide housing, weather, and event info 
* Marketplace for users to buy/sell or exchange services
* Page for residents of specific neighborhoods to communicate with each other
