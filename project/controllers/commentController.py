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
            fullname = request.form["fullname"]
            email= request.form["email"]
            comment= request.form["comment"]
            rate= int(request.form["rate"])
            response = model_comment.create({'fullname': fullname, 'email': email, 'comment': comment, 'rate':rate})

            return redirect(url_for('homepage'))
            
    except Exception as ex:
                return Response(
                    response=json.dumps(
                        {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )

if __name__ == "project":
    app.run(port=80, debug=True)
