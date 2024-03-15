from flask import Flask, flash, render_template, request, url_for, redirect
from util import construct_table, construct_prediction, construct_list, construct_match_card
from opencv import mark_image
from Computer_Vision_Task.model import pipeline
from werkzeug.utils import secure_filename
from sparql import *
import os


app = Flask(__name__, static_url_path="/static")
app.secret_key = "secret key"

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server_address = "http://localhost:3030/TMDB/sparql"
sparql = SPARQLWrapper(server_address)
sparql.setReturnFormat(JSON)

ALLOWED_EXTENSIONS = set(['png'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html", content="Testing")


@app.route("/searchDatabase", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # specific data from forms can be evaluated here
        request.make_form_data_parser()
        data = request.form
        data_list = []
        for i in data.items():
            data_list.append(i)

        return redirect(url_for("result", data=data_list))
    else:
        return render_template("searchDatabase.html")


@app.route("/result/<data>")
def result(data):
    print("data", data)
    data_list = [["asd"], ["qwe"], ["yxc"]]
    data_cat_list = ["first"]
    content = construct_table(data_list, data_cat_list)
    return render_template("searchResult.html", content=content)

@app.route("/countryPredictor", methods=["GET", "POST"])
def computer_vision():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            mark_image("uploads/" + filename)
        else:
            flash('Allowed file type is png')
            return redirect(request.url)

        return redirect(url_for("computer_vision_results"))
    else:
        return render_template("computer_vision.html")
@app.route("/countryResults")
def computer_vision_results():
    content1 = construct_prediction(pipeline("./static/classified_images/yoshiA.png"))
    content2 = construct_prediction(pipeline("./static/classified_images/yoshiB.png"))
    return render_template("computer_vision_results.html", content=[content1, content2])

@app.route("/faq", methods=["GET", "POST"])
def knowledge_graph():
    content0 = construct_list(which_teams_participate_query())
    content1 = construct_table(group_stage_matches_venues_and_capacities(), ['Stadium', 'Capacity'])
    if request.method == "POST":
        return redirect(url_for("countries", data=request.form.get('country')))
    else:
        return render_template("knowledge_graph.html", content=[content0, content1])

@app.route("/moreabout/<country>")
def countries(country):
    ######################### Country name
    country_name = country

    ######################### Matches
    matches_list = custom_match_list_of_x(country_name)
    matches = ""
    for entry in matches_list:
        matches += construct_match_card(entry, country_name)

    ######################### Description of Team
    description = description_of_team_x(country_name)

    ######################### National Squad
    squad = construct_table(who_is_in_the_team_of_x(country_name), ['Player Name'])

    ######################### Trainer
    trainer = who_is_the_coach_of_x_query(country_name)

    ######################### Info about Trainer
    _info_trainer = information_about_coach_x(trainer)
    info_trainer = _info_trainer[0] + ", " + _info_trainer[1]

    ######################### Image Path
    img_path = "../static/images/" + country_name + ".png"

    return render_template("country.html", content=[matches, description, squad, trainer, info_trainer, country_name, img_path])


if __name__ == "__main__":
    app.run(debug=True)
