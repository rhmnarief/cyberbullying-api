
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


# @app.route("/predict_cyberbullying/", methods=["POST"])
# def check_cyberbullying():
#     try:
#         form = request.form
#         input_prediction = form.get("input_prediction")
#         cleaned_text = MachineModel.clean_text(input_prediction)
#         series_text = pd.Series(cleaned_text)
#         preprocessed_text = series_text.apply(MachineModel.preprocess_tweet)
#         vectorized_text = MachineModel.TFIDFVector.transform(preprocessed_text.astype("U"))
#         result_test = MachineModel.model.predict(vectorized_text)
#         final_result = MachineModel.difine_result(result_test)
#         timestamp = datetime.now()

#         prediction = {
#             "inputText": input_prediction,
#             "resultPrediction": final_result,
#             "date": f"{timestamp}",
#         }
#         dbResponse = db.predict_result.insert_one(prediction)

#         return Response(
#             response=json.dumps(
#                 {
#                     "id": f"{dbResponse.inserted_id}",
#                     "message": "Input Succesfully Predicted!",
#                     "inputText": input_prediction,
#                     "resultPrediction":  final_result,
#                     "date": f"{timestamp}",
#                 }
#             ),
#             status=200,
#             mimetype="application/json",
#         )

#     except Exception as ex:
#         print(ex)
#         return Response(
#             response=json.dumps({"message": "Method Post Predict Failed"}),
#             status=500,
#             mimetype="application/json",
#         )