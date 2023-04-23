from flask import Flask, request, jsonify
from search import search
from filter import Filter
from storage import DBStorage
import html

app = Flask(__name__)

styles = """
<style>
    *{
        margin: 0;
        padding: 0;
    }


    body{
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #140e0d;
}

.box{
    height: 30px;
    display: flex;
    cursor: pointer;
    padding: 10px 20px;
    background: #2f3640;
    border-radius: 30px;
    align-items: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);   
}


.box input{
    width: 400px;
    outline: none;
    border: none;
    font-weight: 500;
    color: #e84118;
    font-size: 20px;
    transition: 0.8s;
    background: transparent;
}

.box button{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: white;
    border: none;
}

.search{
 width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: white;
    border: none;
    font-size: 24px; /* increase font size */
    padding: 5px; /
}

.box button .fas{
    color: #e84118;
    font-size: 18px;
    }


    .site {
        font-size: .8rem;
        color: yellow;
    }
    
    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }
    
    .rel-button {
        cursor: pointer;
        color: blue;
    }
    
</style>
<script src="https://kit.fontawesome.com/a6015fd7af.js" crossorigin="anonymous">
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           "query": query,
           "link": link
          })
        });
}
</script>
"""

search_template = styles + """
    <body>
        <div class="box">
            <form action="/" method="post" class="search-bar">
                <input type="text" placeholder="search anything" name="query">
                <button type="submit">
                        <i class="fas fa-search"></i>
                </button>
            </form>
        </div>
    </body>
    """

result_template = """
    <p class="site" style="color:#194d33"><span style="color:red">{rank}:</span> {link}<span class="rel-button" onclick='relevant("{query}", "{link}");' style="cursor: pointer,
                color: blue" >Relevant</span></p>
        <a href="{link}">{title}</a>
        <p class="snippet">{snippet}</p>
    
"""

def show_search_form():
    return search_template


def run_search(query):
    results = search(query)
    fi = Filter(results)
    filtered = fi.filter()
    filtered["snippet"] = filtered["snippet"].apply(lambda x: html.escape(x))
    filtered = filtered.sort_values(by='rank')
    rendered = "<html>" + styles + "<body>"
    rendered += f"""
    <div class="search" style="text-align: center;">
    <form action="/" method="post" class="search-bar">
        <input type="text" placeholder="search anything" name="query" value="{query}" 
       style="border-radius: 10px;
       width: 600px;
       height: 40px;
       border:none;
       font-size: 16px;
       box-shadow: 2px 2px 5px #888888;
       ">
        <button type="submit" style="background-color: #dbdbdb;
                    border: none;
                    border-radius: 25px;
                    color: #f01f1f;
                    padding: 12px 22px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    margin-left:6px;
                    cursor: pointer;">
            <i class="fas fa-search"></i>
            Submit
        </button>
    </form>
</div>

    """
    for index, row in filtered.iterrows():
        rendered += result_template.format(**row)
    rendered += "</body></html>"
    rendered = f'<script>window.open("data:text/html;charset=UTF-8,{rendered}</script>'
    return rendered

@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()

@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)