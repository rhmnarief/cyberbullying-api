# from project.config import *
from flask import Flask
from flask_cors import CORS

app = Flask("project")
CORS(app)

from project.controllers import *
# from project.algorithm import *
# from project.controllers import predictController
# from project.controllers import commentController

if __name__ == "project":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(port=80, debug=True)