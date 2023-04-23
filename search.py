from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
from datetime import datetime
from weight_page_rank import WeightedPageRank
from lang_modelling import LanguageModelling
from urllib.parse import quote_plus

def search_api(query, pages=int(RESULT_COUNT/10)):
    results = []
    print("query",query)
    for i in range(0, pages):
        start = i*10+1
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),
            start=start
        )
        response = requests.get(url)
        data = response.json()
        print("data",data)
        results += data["items"]
    res_df = pd.DataFrame.from_dict(results)
    #print("df",res_df)
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]
    return res_df

def scrape_page(links):
    html = []
    for link in links:
        #print(link)
        try:
            data = requests.get(link, timeout=5)
            html.append(data.text)
        except RequestException:
            html.append("")
    return html

def ParentDict(link,adDict,weightedPageRankDict,langModelling):
    ParentDict={}
    for i in adDict.keys():
        try:
            ParentDict[i]=((adDict[i]*0.4)+(weightedPageRankDict[i]*0.4)+(abs(langModelling[i])*0.2))
        except:
            ParentDict[i]=((adDict[i]*0.4)+(weightedPageRankDict[i]*0.4)+(2))

    return ParentDict.keys(),ParentDict.values()
def search(query):
    columns = ["query", "rank", "link", "title", "snippet", "html", "created"]
    storage = DBStorage()

    stored_results = storage.query_results(query)
    if stored_results.shape[0] > 0:
        stored_results["created"] = pd.to_datetime(stored_results["created"])
        return stored_results[columns]

    print("No results in database.  Using the API.")
    # from API

    results = search_api(query)
    link = results['link']
    rank = results['rank']
    AdDict = dict(zip(link,rank ))
    weightedPageRankDict = WeightedPageRank(link)
    langModelling = LanguageModelling(query,link)

    results['link'],results['rank']=ParentDict(link,AdDict,weightedPageRankDict,langModelling)
    print("Results inside search",type(results['link']))
    
    print("Results inside search",type(results['rank']))
    html = scrape_page(results["link"])
    results["html"] = html
    results = results[results["html"].str.len() > 0].copy()
    results["query"] = query
    results["created"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    results = results[columns]
    results.apply(lambda x: storage.insert_row(x), axis=1)
    #print(f"Inserted {results.shape[0]} records.")
    return results