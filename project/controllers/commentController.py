from project import app
from flask import Response, request, render_template, redirect, url_for, jsonify

from werkzeug.exceptions import HTTPException
import json

from project.models import comment


model_comment = comment.Comment()

@app.route('/comment', methods=['GET'])
def get_comment():
    try:
        return jsonify(model_comment.find({}))
    except Exception as ex:
        return Response(
            response=json.dumps(
                        {
                            "message": "cannot get comment data", 
                            "error": f"{ex}"
                        }
                        ),
                    status=500,
                    mimetype="application/json",
        )

@app.route('/comment', methods=['POST'])
def add_comment():
    try:
        if request.method == "POST":
                if request.form:
                    fullname = request.form["fullname"]
                    email= request.form["email"]
                    comment= request.form["comment"]
                    rate = request.form.get('rate', type=int)
                    result_sent = model_comment.create({'fullname': fullname, 'email': email, 'comment': comment, 'rate':rate})
                    return Response(
                        response=json.dumps({"message": "success send comment data", "response" :result_sent }),
                            status=200,
                            mimetype="application/json",
                    )
                return Response(
                        response=json.dumps({"message": "Form input must be filled"}),
                            status=400,
                            mimetype="application/json",
                    )
            
    except Exception as ex:
                return Response(
                    response=json.dumps(
                        {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )

if __name__ == "project":
    app.run(port=80, debug=True)
