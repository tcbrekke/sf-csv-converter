# Dependencies
#------------------------
from flask import Flask, request, render_template, Response
import pandas as pd 
import os
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


app = Flask(__name__)

# Establish Database Connection
#------------------------

# DATABASE_URL = os.environ['DATABASE_URL']
# engine = create_engine(DATABASE_URL)
# connection = engine.connect()

# Base = automap_base()
# Base.prepare(engine, reflect=True)
# session = Session(engine)

# Flask Routes
#------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload.html", methods = ['POST'])
def upload_route_summary():
	if request.method == 'POST':

		# converted_path = os.path.join("resources", "converted.csv")
		# Create variable for uploaded file
		csv_to_convert = request.files['csvupload'] 

		content_df = pd.read_csv(csv_to_convert).reset_index()
		icap = len(content_df)
		print(icap)

		titles = []
		posts = []
		dates = []
		times = []
		labels = []
		channels = []

		i = 0
		print("first check")

		while i < icap:
		    print(f"Start no. {i}")
		    if content_df.iloc[i]["Auto Imported"] == "no":
		        j = i+1
		        k = i+2
		        current_post_dict = {}
		        title = content_df.iloc[i]['Title']
		        post_text = content_df.iloc[i]['Content']
		        pub_date = content_df.iloc[i]["Date"]
		        pub_time = content_df.iloc[i]["Time"]
		        all_labels = content_df.iloc[i]["Labels"].split(",")

		        for label in all_labels:
		            if label[:16] == "Dolby Initiative":
		                primary_label = label

		        post_channels = content_df.iloc[i]["Accounts"]
		        print("got here")

		        if (len(content_df)) >= (j):
		            if content_df.iloc[j]["Title"] == title:
		                new_channels = content_df.iloc[j]["Accounts"]
		                print(f"Check out these new channels: {new_channels}")
		                post_channels = f"{post_channels},{new_channels}"
		#                 See if next cell exists, then if it is also a duplicate
		                if (len(content_df)) >= k:
		                    if content_df.iloc[k]["Title"] == title:
		                        new_channels = content_df.iloc[k]["Accounts"]
		                        post_channels = f"{post_channels},{new_channels}"
		                        i += 3
		                    else:
		#                         current_post_dict["title"] = title
		#                         current_post_dict["post content/description"] = post_text
		#                         current_post_dict["publish date"] = pub_date
		#                         current_post_dict["publish time"] = pub_time
		#                         current_post_dict["labels"] = primary_label
		#                         current_post_dict["channel"] = channels
		#                         current_post_df = pd.DataFrame(current_post_dict, index=[0])
		#                         converted_df.append(current_post_df)
		                        i += 2
		            else:
		                i += 1

		        titles.append(title)
		        posts.append(post_text)
		        dates.append(pub_date)
		        times.append(pub_time)
		        labels.append(primary_label)
		        channels.append(post_channels)
		    else:
		        i = i + 1

	new_csv_dict = {"title": titles, "post content/description": posts, "publish date": dates, "publish time": times, "labels": primary_label, "channel": channels}
	new_df = pd.DataFrame(new_csv_dict)

	modified_csv = new_df.to_csv()

	return Response(modified_csv, mimetype="text/csv", headers={"Content-Disposition":"attachment; filename=converted.csv"})

if __name__ == "__main__":
    app.run(debug=True)