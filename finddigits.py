import json
from tokenize import String
import requests
from flask import Flask, Request, Response, jsonify, request
import base64


app = Flask(__name__)


def findDigits(n):
    count = 0
    lst = str(n)
    for x in lst:
        if int(x) != 0 and n % int(x) == 0:
            count += 1
    return count

@app.route('/find-digits2', methods=['POST'])
def handler2():
    lst = []
    req = request.get_json()['check']
    for x in range(len(req)):
        output = {
            'input' : req[x],
            'output' : findDigits(req[x])
        }
        lst.append(output)
    return {'result': lst }

    