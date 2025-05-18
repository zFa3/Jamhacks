from flask import render_template, Blueprint, request, jsonify
from gemini_api_call import Interface
import json

views = Blueprint("views", __name__)

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/get-data")
def get_data():
    data_informations = None
    with open("web_data_viewer/sent_data.json", "r") as file:
        data_informations = json.load(file)
    
    # print(jsonify(data_informations))
    return jsonify(data_informations)

@views.route("/get-gemini/<graph>")
def get_gemini(graph):
    # data_array = data_array.replace("&", ",").replace("d", ".")
    with open("web_data_viewer/sent_data.json", "r") as file:
        data_informations = json.load(file)
    if graph == "eyeGraph":
        response = Interface().generate(f"max 20 words: find the mean of this data set, which contain values that represent the direction a driver looks at during a trip. {data_informations["left_pan"]}")
    elif graph == "tiltGraph":
        response = Interface().generate(f"within 20 words, find the mean of this data set {data_informations["head_tilt"]}")
    else:
        max_value = max(data_informations["phone_detected"])
        response = Interface().generate(f"within 20 words, how bad is it that i looked at my phone {max_value} when driving")

    return jsonify({"output": response})
