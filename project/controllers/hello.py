"""
    Example Controllers
"""

from project.algorithm import MachineModel
from project import app
from project.config import Database

from flask import Response, request, render_template, redirect, url_for, jsonify
from werkzeug.exceptions import HTTPException
from bson.objectid import ObjectId
from datetime import datetime


import pandas as pd
import json
import requests
from dotenv import load_dotenv
import os
"""
    Import MOdels
from project.models.Hello import Hello
"""
# route index


load_dotenv()

db = Database.db


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("/error/404.html", exception=e), 404


@app.route('/', methods=['GET'])
def homepage():
    try:
        url = request.host_url + "comments"
        get_comment = requests.get(url)
        response_json = get_comment.json()
        return render_template(
            '/pages/home.html',
            data_comment=response_json
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read comment"}),
            status=500,
            mimetype="application/json",
        )

#########


@app.route("/guide")
def guide():
    try:
        data_guide = [
            {
                "title": "Register Your API Key",
                "description": "API key is used to identify yourself as a valid client, set access permissions, and record your interactions with the API. you’ll most likely need to sign up with the service. You’ll then have a unique identifier assigned to you, which you will include in your calls.",
            },
            {
                "title": "Read Documentation",
                "description": " We are providing all the information required to in the documentation for how to get your key, how to send requests, and which resources you can fetch from its server.",
            },
            {
                "title": "Write a request to an endpoint",
                "description": "Use the best method for use HTTP client to help structure and send your requests. You’ll still need to understand and get some information from the API’s documentation, but you won’t need much coding knowledge to be successful.",
            },
            {
                "title": "Connect your app",
                "description": " You can sync your application with it. As a marketer, you don't need to worry about this stage of an API integration. This is the job of a developer, who will employ one or more languages like Python, Java, JavaScript (and NodeJS), PHP, and more.",
            },
        ]
        url = request.host_url + "predict_cyberbullying"
        return render_template(
            '/pages/guide.html',
            data_url=url,
            data_guide=data_guide
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "guide error", "error": f"{ex}"}),
            status=500,
            mimetype="application/json",
        )


# Model Section
@app.route("/predict", methods=["POST", "GET"])
def predict():
    if request.method == "POST":
        try:
            form = request.form
            input_prediction = form.get("input_prediction")
            cleaned_text = MachineModel.clean_text(input_prediction)
            series_text = pd.Series(cleaned_text)
            preprocessed_text = series_text.apply(
                MachineModel.preprocess_tweet)
            vectorized_text = MachineModel.TFIDFVector.transform(preprocessed_text.astype("U"))
            result_test = MachineModel.model.predict(vectorized_text)
            final_result = MachineModel.difine_result(result_test)
            return render_template("/pages/detection.html", result=final_result, input=input_prediction)
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


@app.route("/predict_cyberbullying/", methods=["POST"])
def check_cyberbullying():
    try:
        form = request.form
        input_prediction = form.get("input_prediction")
        cleaned_text = MachineModel.clean_text(input_prediction)
        series_text = pd.Series(cleaned_text)
        preprocessed_text = series_text.apply(MachineModel.preprocess_tweet)
        vectorized_text = MachineModel.TFIDFVector.transform(preprocessed_text.astype("U"))
        result_test = MachineModel.model.predict(vectorized_text)
        final_result = MachineModel.difine_result(result_test)
        timestamp = datetime.now()

        prediction = {
            "inputText": input_prediction,
            "resultPrediction": final_result,
            "date": f"{timestamp}",
        }
        dbResponse = db.predict_result.insert_one(prediction)

        return Response(
            response=json.dumps(
                {
                    "id": f"{dbResponse.inserted_id}",
                    "message": "Input Succesfully Predicted!",
                    "inputText": input_prediction,
                    "resultPrediction":  final_result,
                    "date": f"{timestamp}",
                }
            ),
            status=200,
            mimetype="application/json",
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Method Post Predict Failed"}),
            status=500,
            mimetype="application/json",
        )

#########
# CRUD Section


@app.route("/comments", methods=["POST", "GET"])
def manage_comment():
    if request.method == "GET":
        def get_comment():
            try:
                data = list(db.comments.find())
                for comment in data:
                    comment["_id"] = str(comment["_id"])
                return Response(
                    response=json.dumps(
                        data, indent=4, sort_keys=True, default=str),
                    status=200,
                    mimetype="application/json",
                )
            except Exception as ex:
                print(ex)
                return Response(
                    response=json.dumps(
                        {"message": "cannot get comments data", }),
                    status=500,
                    mimetype="application/json",
                )
        return get_comment()
    if request.method == "POST":
        def send_comment():
            try:
                comment = {
                    "fullname": request.form["fullname"],
                    "email": request.form["email"],
                    "comment": request.form["comment"],
                    "rate": request.form["rate"],
                    "timestamp": datetime.now(),
                }
                dbResponse = db.comments.insert_one(comment)

                send_response = Response(
                    response=json.dumps(
                        {"message": "comment sent",
                         "id": f"{dbResponse.inserted_id}"
                         }
                    ),
                    status=200,
                    mimetype="application/json",
                )

                return redirect(url_for('homepage'))
            except Exception as ex:
                return Response(
                    response=json.dumps(
                        {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )
        return send_comment()


# @app.route("/users/<id>", methods=["PATCH"])
# def update_user(id):
#     try:
#         dbResponse = db.users.update_one(
#             {"_id": ObjectId(id)},
#             {"$set": {"name": request.form["name"]}}
#         )

#         if dbResponse.modified_count == 1:
#             return Response(
#                 response=json.dumps(
#                     {"message": "user updated!", }
#                 ),
#                 status=200,
#                 mimetype="application/json",
#             )
#         else:
#             return Response(
#                 response=json.dumps(
#                     {"message": "nothing updated!", }
#                 ),
#                 status=200,
#                 mimetype="application/json",
#             )

#     except Exception as ex:
#         print("*************")
#         print(ex)
#         print("*************")
#         return Response(
#             response=json.dumps(
#                 {"message": "sorry cannot update user", }
#             ),
#             status=500,
#             mimetype="application/json",
#         )
# #########


# @app.route("/users/<id>", methods=["DELETE"])
# def delete_user(id):
#     try:
#         dbResponse = db.users.delete_one({"_id": ObjectId(id)})
#         if dbResponse.deleted_count == 1:
#             return Response(
#                 response=json.dumps(
#                     {
#                         "message": "success deleted data user!",
#                         "id": f"{id}"
#                     }
#                 ),
#                 status=200,
#                 mimetype="application/json",
#             )
#         else:
#             return Response(
#                 response=json.dumps(
#                     {
#                         "message": "user not found!",
#                     }
#                 ),
#                 status=200,
#                 mimetype="application/json",
#             )
#     except Exception as ex:
#         print("*************")
#         print(ex)
#         print("*************")
#         return Response(
#             response=json.dumps(
#                 {"message": "data user cannot be deleted", }
#             ),
#             status=500,
#             mimetype="application/json",
#         )

#########


# @app.route('/send-auth', methods=["POST"])
# def send_auth():
    # try:
    #     form = request.form
    #     receipents_email = form.get("email_user")
    #     set_message = Message(
    #         "Authentication Key", sender='noreply@demo.com', recipients=os.getenv("MAIL_USERNAME"))
    #     set_message.body = "Hello! is everything fine?"
    #     mail.send(set_message)
    #     return Response(
    #         response=json.dumps({"message": "Auth Key has Sent to ", }),
    #         status=200,
    #         mimetype="application/json",
    #     )

    # except Exception as ex:
    #     print("*************")
    #     print(ex)
    #     print("*************")
    #     return Response(
    #         response=json.dumps(
    #             {"message": "Error, cannot send API authentication", }
    #         ),
    #         status=500,
    #         mimetype="application/json",
    #     )


if __name__ == "__main__":
    app.run(port=80, debug=True)
