import requests
from bs4 import BeautifulSoup
import numpy as np

def WeightedPageRank(urls):
    
    def WebGraph(url):
        links = []

        # Loop through the URLs and scrape each page for hyperlinks
        for url in urls:
            # Send a GET request to the URL
            response = requests.get(url)
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all the <a> tags on the page
            a_tags = soup.find_all('a')
            # Extract the href attribute of each <a> tag
            hrefs = [a.get('href') for a in a_tags]
            # Add the list of hrefs to the links list
            links.append(hrefs)
        #    print(links)

        # Create the web graph matrix
        n = len(urls)
        web_graph = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if urls[j] in links[i]:
                    web_graph[i, j] = 1

        #print(web_graph)
        return web_graph


    def win(matrix, m, o):
        k = 0
        for i in range(0, n):
            if(int(matrix[i][m]) == 1):
                k = k+1
        l = 0
        for i in range(0, n):
            if(int(matrix[o][i] == 1)):
                for j in range(0, n):
                    if(matrix[j][i] == 1):
                        l = l+1
        if(l!=0):
            return float(k/l)
        else:
            return 1


    def wout(matrix, m, o):
        k = 0
        for i in range(0, n):
            if(int(matrix[0][i]) == 1):
                k = k+1
        l = 0
        for i in range(0, n):
            if(int(matrix[o][i] == 1)):
                for j in range(0, n):
                    if(matrix[i][j] == 1):
                        l = l+1
        if(l!=0):
            return float(k/l)
        else:
            return 1


    def pagerank(matrix, o, n, p):
        a = 0
        for i in range(0, n):
            if(int(matrix[i][o]) == 1):
                k = 0
                for s in range(0, n):
                    if(matrix[i][s] == 1):
                        k = k+1
                if(k!=0):
                    a = a+float((p[i]/k)*win(matrix, i, o)*wout(matrix, i, o))
        return a



    o = 5
    p = []
    d = 0.25
    web_graph=WebGraph(urls)
    n=len(urls)

    def Score(n,web_graph,urls):
        dic1={}
        for i in range(0, n):
            p.append(1)
        for k in range(0, o):
            for u in range(0, n):
                g = pagerank(web_graph, u, n, p)
                p[u] = (1-d)+d*g
        for i in range(0, n):
            dic1[urls[i]]= p[i]
            #print("Page rank of node ", i+1, "is : ", p[i])
        return dic1

    dic=Score(n,web_graph,urls)
    return dic
    