from project import app

from flask import Response, flash, request, render_template, redirect, url_for, jsonify
from werkzeug.exceptions import HTTPException

import json
import requests


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
        # Hit Endpoint [GET] COMMENT
        url_get_comment = request.host_url + "comment"
        hit_get_comment = requests.get(url_get_comment)
        response_get_comment = hit_get_comment.json()

        return render_template(
            '/pages/home.html',
            data_comment=response_get_comment,
        )
    except Exception as ex:
        return Response(
            response=json.dumps({"message": "cannot read comment", 'error' : f"{ex}"}),
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


@app.route('/notification', methods=['GET', 'POST'])
def notification():
    if request.method == "GET":    
        return render_template('test.html')
    if request.method == "POST":
        flash('Your comment has been sent||Sugestion', 'success')
        return redirect(url_for('homepage'))

