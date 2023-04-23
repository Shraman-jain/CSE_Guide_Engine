
# CSE_Guide_Engine

To Run this flask web application first run

```pip install -r requirements.txt 
```
to install all of the Python modules and packages listed in your requirements.txt file

and then run flask app on localhost by 

```
flask --debug run --port 5001
```


File overview:

1) app.py - contains main code for flask app.
2) search.py - contains a code where user’s query will be searched on the web.
3) filter.py - have code for filtering the results on ads and proxy websites.
4) lang_modelling.py - contains a code for filtering the result on the basis of language modelling score.
5) weight_page_rank.py -  contains a code for filtering the result on the basis of weighted page rank score. 
6) storage.py - contains code for storing the result into database.
7) blacklist.txt - contains list of all proxy websites.
links.db -  SQLite database file where results are stored.
8) Deploy Link: https://8642-103-25-231-102.ngrok-free.app/
The deploy link is only valid for 24 April midnight. If needed we will generate another deploy link at the time of presentation. The project can also be run on local host.
