# transferMarktScraper

www.transfermarkt.com scraper

## Getting Started

With these instructions you can create your environment and run in your local machine.

### Prerequisites

You need python3 on your machine to run this project:

```
sudo apt-get install python3
```

If pip3 does not install via python3 install:

```
sudo apt-get install pip3
``` 

Firefox geckodriver installation:

https://github.com/mozilla/geckodriver/releases

Python3 geckodriver usage:

![gecko_implement_image](https://image.ibb.co/h9BXGo/gecko_implement.jpg)

After that you need libraries for project:

```
pip3 install selenium
pip3 install pynput
pip3 install json
pip3 install datetime
```

## Running the tests

log.txt file holds the last read in that system. This way you do not need to start from the first data.

## For presentation: 

players.json holds:

* Player name
* Date of birth
* Nationality
* Position
* Current club
* Loan club (if exists)
* Price

teams.json holds:

* Team name
* Team's country
* Team's league
* Total value

results.json holds:

* Match date
* Which league was the match for?
* Home team name
* Visitor team name
* Home total goal(s)
* Visitor total goal(s)
* Full time result




  
