from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)