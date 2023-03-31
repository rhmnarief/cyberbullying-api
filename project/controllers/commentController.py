from project import app
from flask import Response, request, render_template, redirect, url_for, jsonify, flash
import requests


from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_parameter, get_page_args

import json

import math

from project.models import comment


model_comment = comment.Comment()

@app.route('/count-comment', methods=['GET'])
def count_data():
    try:
        total = model_comment.count()

        response_endpoint = Response(
                        response=json.dumps({"message": "succes get data", 'total_data' : total}),
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
        args = request.args
        skip = args.get("skip", default=0, type=int)
        limit = args.get("limit", default=5, type=int) 

        sorted = ["rate", -1]

        total = model_comment.count()
        total_page = total - skip 
        next_skip = skip + limit
        prev_skip = skip - limit

        next_url = '/?skip=' + str(next_skip) + '&limit=' + str(limit)
        prev_url = '/?skip=' + str(prev_skip) + '&limit=' + str(limit)  

        if prev_skip < 0 :
            prev_url = None
            prev_skip = 0

        if total_page < limit:
            next_url = None
       
        response_get_comment= jsonify({
                        'data' : model_comment.find({}, sorted, skip, limit), 
                        'next_url' :next_url, 
                        'previous_url' :prev_url,
                        'total_data': total_page
                        })

        return response_get_comment

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

@app.route('/check-email', methods=['POST'])
def email_check():
    try:
        url = "https://api.reacher.email/v0/check_email"
        email = request.form["email"]
        headers = {"content-type": "application/json", 'authorization': 'a63be4aa-a6fd-11ed-bedf-f73f2d8f00b6'}
        payload = {"to_email": email}
        request_email = requests.post(url, json=payload, headers=headers)
        data = request_email.json()
        print(data)
        if data['is_reachable'] == "safe":
             return 'true'
        else:
             return 'false'
        

    except Exception as ex:
        json_response = Response(
        response=json.dumps( {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )
        return json_response
     

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
                    
                    url = "https://api.reacher.email/v0/check_email"
                    email = request.form["email"]
                    headers = {"content-type": "application/json", 'authorization': 'a63be4aa-a6fd-11ed-bedf-f73f2d8f00b6'}
                    payload = {"to_email": email}
                    request_email = requests.post(url, json=payload, headers=headers)
                    data = request_email.json()

                    if data['syntax']['is_valid_syntax']:
                          if data['is_reachable'] == "safe":
                                result_sent = model_comment.create({'fullname': fullname, 'email': email, 'comment': comment, 'rate':rate})
                                response_endpoint = Response(
                                    response=json.dumps({"message": "success send comment data", "response" :result_sent }),
                                        status=200,
                                        mimetype="application/json",
                                )
                                flash('Your comment has been sent||Success Sent Comment!', 'success')
                                return redirect(url_for('homepage'))
                          else:
                                flash('Your Email Is Not Verified||Failed Sent Comment!', 'warning')
                                return redirect(url_for('homepage'))
                    else:
                        flash('Your Input Email Syntax Is Not Corrected||Failed Sent Comment!', 'warning')
                        return redirect(url_for('homepage'))

    except Exception as ex:
                json_response = Response(
                    response=json.dumps(
                        {"message": "cannot send comment data", "error": f"{ex}"}),
                    status=500,
                    mimetype="application/json",
                )
                flash(f"{ex}", 'error')
                return redirect(url_for('homepage'))

