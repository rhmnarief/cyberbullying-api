# from project.config import *
from flask import Flask
from flask_cors import CORS

app = Flask("project")
CORS(app)

from project.controllers import *
# from project.algorithm import *
# from project.controllers import predictController
# from project.controllers import commentController
