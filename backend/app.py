from flask import Flask, request, jsonify, make_response
import mysql.connector
import logging

app = Flask(__name__)
