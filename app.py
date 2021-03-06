import os
from flask import Flask, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('DATABASE')

if os.path.exists("env.py"):
    app.config["MONGO_URI"] = env.mongo_uri
else:
    app.config["MONGO_URI"] = os.environ.get('MONGO_URI')


app.secret_key = 'some_secret'

mongo = PyMongo(app)

app.templates = ""


# this is a helper for the Live Links.  You can ignore these!
@app.route('/lesson/<lesson>')
def lessons(lesson):
    return render_template("lessonspleaseignore/"+lesson+'.html')


# This is for your index Page!  Cool!  You should always have one of these.  It is the ('/') is the base root.
@app.route('/')
def index():
    return render_template('index.html')


# This is a General Routing.  But leads you to a form.  You will notice that this takes no input.
# As we have not methods attached this is a get method.
@app.route('/add')
def addTest():
    return render_template('addtask.html')


# This is a POST method and comes from posting a form. In this example We are adding a new entry to our database once a form is submitted.
# Once we add the value, I am running a print test to show the value returned :)  Then I use a redirect to return to the homepage
@app.route('/inserttest', methods=['POST'])
def insert_test():
    test = mongo.db.mongoTestingDataBase
    inserted_value=test.insert(request.form.to_dict())
    print(inserted_value)
    print(test.find({'_id':inserted_value}))
    return redirect(url_for('index'))


@app.route('/edittest/<test_id>', methods=["GET", "POST"])
def edit_test(test_id):
    test = mongo.db.mongoTestingDataBase.find_one({"_id" : ObjectId(test_id)})
    print(test)
    return render_template("a_test.html", test=test)

@app.route('/search')
def search():
    query = request.args.get("q")
    results = mongo.db.mongoTestingDataBase.find({"testname" : {"$regex": query}})
    return render_template("search.html", results=results)


def get_tests(offset=0, per_page=10):
    thetests = mongo.db.mongoTestingDataBase.find()
    print("herl")
    return thetests[offset: offset + per_page]

@app.route('/here')
def showTests():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = mongo.db.mongoTestingDataBase.find().count()
    paginatedTests = get_tests(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('thetests.html',
                           tests=paginatedTests,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )



# The correct running of you app file :)  In terms of Environmental Variables on Heroku.   0.0.0.0  Is the IP and 5000 for Port
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)