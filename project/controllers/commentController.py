from asyncio.windows_events import NULL
from project import app
from flask import Response, request, render_template, redirect, url_for, jsonify, flash

from werkzeug.exceptions import HTTPException
import json

from project.models import comment


model_comment = comment.Comment()

@app.route('/count-comment', methods=['GET'])
def count_data():
    try:
        counted = model_comment.count()
        response_endpoint = Response(
                        response=json.dumps({"message": "succes get data", 'total_data' : counted}),
                            status=200,
                            mimetype="application/json",
                    )
        return response_endpoint
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


@app.route('/comment', methods=['GET'])
def get_comment():
    try:
        sorted = "rate"
        ascending = -1
        limit = 5
        return jsonify(model_comment.find({}, sorted, ascending, limit))
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
                    
                    if request.form["fullname"] == "" or request.form["email"] == "" or request.form["comment"] == "" or request.form["rate"] == NULL:
                        response_endpoint = Response(
                                response=json.dumps({"message": "Form input must be filled"}),
                                    status=400,
                                    mimetype="application/json",
                            )
                        flash('Form Not Fullfill||Form input must be filled!', 'warning')
                        return redirect(url_for('homepage', message = response_endpoint))

                    result_sent = model_comment.create({'fullname': fullname, 'email': email, 'comment': comment, 'rate':rate})
                    response_endpoint = Response(
                        response=json.dumps({"message": "success send comment data", "response" :result_sent }),
                            status=200,
                            mimetype="application/json",
                    )
                    flash('Your comment has been sent||Success Sent Comment!', 'success')
                    return redirect(url_for('homepage'))

               
            
    except Exception as ex:
                flash(f"{ex}", 'error')
                return redirect(url_for('homepage'))
                return Response(
                    response=json.dumps(
                        {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )

