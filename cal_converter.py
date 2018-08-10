# Dependencies
#------------------------
from flask import Flask, render_template
import pandas as pd 
import os
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


app = Flask(__name__)

# Establish Database Connection
#------------------------

DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
connection = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

# Flask Routes
#------------------------

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("upload.html", methods = ['POST'])
# def upload_route_summary():
#     if request.method == 'POST':

#         # Create variable for uploaded file
#         f = request.files['csvupload'] 

if __name__ == "__main__":
    app.run(debug=True)