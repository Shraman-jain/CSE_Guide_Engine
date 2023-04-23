
# CSE_Guide_Engine

## Project overview 

In this project, we'll build a search engine that uses filtering to reorder results. The engine will get search results, store them, then rank them based on filters we define. We'll end up with a basic search page and results list.

## Installation

To follow this project, please install the following locally:

`Python:3.9+`

```
pip install -r requirements.txt 
```
## Run
To install all of the Python modules and packages listed in your requirements.txt file

and then run flask app on localhost by 

```
flask --debug run --port 5001
```


## File overview:

`app.py` - contains main code for flask app.

`search.py` - contains a code where user’s query will be searched on the web.

`filter.py` - have code for filtering the results on ads and proxy websites.

`lang_modelling.py` - contains a code for filtering the result on the basis of language modelling score.

`weight_page_rank.py` -  contains a code for filtering the result on the basis of weighted page rank score. 

`storage.py` - contains code for storing the result into database.

`blacklist.txt` - contains list of all proxy websites.

`links.db` -  SQLite database file where results are stored.
## Links 
`Deploy Link` [CSEngine](https://8642-103-25-231-102.ngrok-free.app/)

This project is deployed on ngrok and it may expire by the time of presentation. We can still run the project on local host or deploy again to genrate new URL.
