# Data Engineering Time Series Challenge

## Intro

Swissgrid is building a dedicated time series database and therefore wants you to do a scalabe Minimal Viable Product. 
You get provided a sample dataset of the "to be frequency of the grid" for 2 months in 30sec resolution. Design the solution so it is scalable to hundreds of such timeseries from 15 min resolution to secondly resolutions.
The goal of the challenges is to ingest the sample data set effeciently into this database and put a asynchronous API framework of your choice on top to query the data to provide data for different applications.


**Please invest no more than 6 to 8 hours.**

If you cannot complete the task in this time frame, document where you got stuck, so we can use this as a basis for
discussion for your next interview.

## Your challenge in a nutshell:

### Starting Point

* sample timeseries in this repository in CSV format
* Preferred & already in place programming language is python although you can use different languages & technologies if you can argument it
* Your solution has be packaged so we can run it(this is part of the challenge), so either use containers or language specific builds

### Abstract solution design

```mermaid
  flowchart TD
    (CSV or other fileformat) -- Ingest Logic ---tsdb[(TS Database)] <--> api[async API] <--> app[application]
```

### Step 1

* Make technology choices for the database and the API framework and document why you chose them(Hint: we like [adrs](https://adr.github.io/)).

### Step 2

* Start and configure database 
* Ingest data to database
* Write API component to query data
* Test both components 

## Evaluation criteria

What we're looking for:

* Clean project setup
* The ability to determine the actual problem area and find a suitable solution
* Relevant tests for your code
* Scratch features when necessary, time is short!
* Document your approach, your decisions, and your general notes

## Preparations for interview

* open your IDE
* have a running version of your app ready
* prepare to present your approach for 5-10 min (no slides!)
* be prepared to answer a few questions after your presentation