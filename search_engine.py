from __future__ import print_function
from flask import Flask, render_template, request
import os
from flask_pymongo import PyMongo
from Document.get_document import read_json
from handle_query import Query
from time import time

BOOKKEEPING_PATH = os.path.join(
    os.getcwd(), 'WEBPAGES_RAW', "bookkeeping.json")
LOOKUP = read_json(BOOKKEEPING_PATH)
DEBUG = True #FOR PRINTING
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MONGO_HOST"] = "***REMOVED***" #"127.0.0.1"
app.config["MONGO_DBNAME"] = "invertedIndex"
app.config["MONGO_USERNAME"] = "***REMOVED***"
app.config["MONGO_PASSWORD"] = "***REMOVED***"
app.config["MONGO_CONNECT"] = True
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


#https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
@app.route('/', methods=['GET', 'POST'])
def query_post():
    if DEBUG:
        print(request.method)
        print(request.form['queryField'])
    # print('This error output', file=sys.stderr)
    # print('This standard output', file=sys.stdout)
    print(request.form['queryField'])
    if len(request.form['queryField']) == 0 and DEBUG:
        print("EMPTY!!!")
    if request.form['queryField'] is not None:
        start = time()
        search_query = request.form['queryField'].lower()
        query_results = Query(search_query, mongo.db).handle()
        if DEBUG:
            print(query_results)
        if query_results is not None:
            list_of_urls = [LOOKUP[doc_id] for doc_id in query_results]
            time_taken = round(time() - start, 3)
            return render_template('index.html', 
                query=request.form['queryField'], posts=list_of_urls, time=time_taken)
        else:
            return render_template('index.html', noResult=search_query)




if __name__ == "__main__":
    app.run()