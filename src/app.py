from flask import Flask, request, g, make_response
from flask_jsonpify import jsonify
from data import data1 as data
from estimator import estimator
from dicttoxml import dicttoxml
import time

app = Flask(__name__)


@app.route("/api/v1/on-covid-19", methods=["GET"])
def default_api():
    return jsonify(estimator(data))


@app.route("/api/v1/on-covid-19/json", methods=["GET"])
def json_api():
    **response(request.method, "/api/v1/on-covid-19/json", 200, 20)
    return jsonify(estimator(data))


@app.route("/api/v1/on-covid-19/xml", methods=["GET"])
def xml_api():
    print(request.path)
    print(request.url)
    xml = dicttoxml(estimator(data))
    return xml


@app.route("/api/v1/on-covid-19/log", methods=["GET"])
def send_log():
    message = ""
    with open("log.txt", "r") as file_ref:
        lines = file_ref.readlines()
        for line in lines:
            message = message + line + "<br>"
        return message


@app.before_request
def commence_timing():
    pass


@app.after_request
def end_timing():
    pass


if __name__ == "__main__":
    app.run()
