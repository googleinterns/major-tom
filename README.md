# Road Rules Search Engine
This repository contains the code and Docker Images of our road regulations search engine.

## Why a road regulations search engine?
Finding accurate and up to date information online is not easy for everybody, especially when it comes to the law. There is no simple way of searching long documents for a specific articles without matching the text completly or having to only use keywords. Our search engine allows users to do complete sentence queries and get articles that match what they are searching for with high accurracy.

## How? 
Our application is divided into multiple microservices to be language agnostic. Also, our apps are containerized so that they can run everywhere, on-prem, cloud, hybrid, etc. 

### Frontend
A React App that connects to the backend and serves content to the user.
### Backend
A Node.js backend that connects to the front end using GraphQL.
### Keywords
Using Google Cloud's Natual Language Processing Engine, the keywords service extracts keywords from text and returns them.
### Search Engine
The search engine is responsible of interpreting queries and connecting with other services to retrieve the matching articles.
### Parser/Database
The parser was responsible of downloading, parsing and saving the document's articles. Then the database endpoint was responsible of interacting with the database and returning all articles and keywords per the queries of other services.
