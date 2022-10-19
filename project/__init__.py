# from project.config import *
from flask import Flask
from flask_cors import CORS

app = Flask("project")
CORS(app)

# from project.algorithm import *
from project.controllers import *
