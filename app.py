import get_domain_cert
import json
from flask import Flask, request

app = Flask(__name__)

@app.route("/get_cert_info", methods=["GET"])
def get_cert_info():
    names = request.args.getlist('name')
    data = get_domain_cert.get_domain_name_cert(names)
    return json.dumps(data, indent=2)
    