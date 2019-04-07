from flask import Flask, jsonify
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

app = Flask(__name__)

@app.route("/")
def hello(): 
    return jsonify({"about": "Hello World!"})

@app.route("/bookList")
def bookList(): 
    get_books()
    file = open('bookList.txt', 'r')
    lines = file.read().split("\n")
    
    response = jsonify(lines)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

def simple_get(url): 
    try: 
        with closing(get(url, stream=True)) as resp: 
            if is_good_response(resp): 
                return resp.content
            else: 
                return None

    except RequestException as e: 
        log_error("Error using requests to {0} : {1}".format(url, str(e)))

def is_good_response(resp): 
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_books():
    url = 'https://www.goodreads.com/user_challenges/16171692'
    response = simple_get(url)

    file = open('bookList.txt','w') 
    
    soup = BeautifulSoup(response, 'html.parser')

    if response is not None: 
        
        for li in soup.find_all('li', attrs={'class': 'bookCoverContainer'}):
            title = li.find('img', alt=True)
            link = li.find('a', attrs={'class': 'bookCoverTarget'})
            
            if title['alt'] is not "":
                file.write(title['alt'] + ' ,link: ' + "https://www.goodreads.com" + link['href'] + '\n')
    
    file.close()