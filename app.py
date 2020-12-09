import mariadb
from flask import Flask, request, Response
from flask_cors import CORS
import json
import dbcreds
import datetime
import secrets

app = Flask(__name__)
CORS(app)