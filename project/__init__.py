# from project.config import *
from flask import Flask
from flask_cors import CORS

app = Flask("project")
CORS(app)


from project.controllers import commentController
from project.controllers import predictController
from project.controllers import mainController
# from project.algorithm import *
# from project.controllers import predictController

if __name__ == "project":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(host="0.0.0.0",port=3001, debug=True)