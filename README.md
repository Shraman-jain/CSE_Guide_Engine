
# CSE_Guide_Engine

To Run this flask web application first run

```
pip install -r requirements.txt 
```
to install all of the Python modules and packages listed in your requirements.txt file

and then run flask app on localhost by 

```
flask --debug run --port 5001
```


File overview:

`app.py` - contains main code for flask app.

`search.py` - contains a code where user’s query will be searched on the web.

`filter.py` - have code for filtering the results on ads and proxy websites.

`lang_modelling.py` - contains a code for filtering the result on the basis of language modelling score.

`weight_page_rank.py` -  contains a code for filtering the result on the basis of weighted page rank score. 

`storage.py` - contains code for storing the result into database.

`blacklist.txt` - contains list of all proxy websites.

`links.db` -  SQLite database file where results are stored.
## links 
`Deploy Link` [![CseGuideEngine]](https://8642-103-25-231-102.ngrok-free.app/)

This project is deployed on ngrok and it may expire by the time of presentation. We can still run the project on local host or deploy again to genrate new URL.
