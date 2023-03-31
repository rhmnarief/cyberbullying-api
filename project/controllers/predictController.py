from project import app
from flask import Response, request, render_template, redirect, url_for, jsonify

from werkzeug.exceptions import HTTPException
import json

from project.models import predict

model_predict = predict.Predict()


# Model Section
@app.route("/predict", methods=["POST"])
def send_predict():
    if request.method == "POST":
        try:
            input_prediction = request.form["input_prediction"]
            result = model_predict.classify(input_prediction)
            return render_template("/pages/detection.html", result=result, input=input_prediction)
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "Method Post Predict Failed"}),
                status=500,
                mimetype="application/json",
            )
    if request.method == "GET":
        return redirect("/")

# Model API

@app.route("/predict_cyberbullying", methods=["POST"])
def check_cyberbullying():
    if request.method == "POST":
        try:
            if request.form:
                input_text = request.form["input_text"] 
            else:
                input_text = request.json['input_text']

            if input_text == "" or input_text is None:
                return Response(
                        response=json.dumps({"message": "Input cannot be empty"}),
                        status=400,
                        mimetype="application/json",
                    )

            result_prediction = model_predict.classify(input_text)
            result_sent = model_predict.create({"input_text":input_text, "result_prediction":result_prediction})
            return Response(
                            response=json.dumps({"message": "success send predict data", 
                            "type_cyberbullying" :result_prediction , 
                            "input_text" :input_text,
                            "status" :result_sent  }),
                            status=200,
                            mimetype="application/json",
                )
                
        except Exception as ex:
            return Response(
                response=json.dumps({"message": f"{ex}", "Type" : "error"}),
                status=500,
                mimetype="application/json",
            )

    if request.method == "GET":
        return Response(
                response=json.dumps({"message": "Bad Request"}),
                status=400,
                mimetype="application/json",
            )