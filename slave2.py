from flask import Flask, jsonify
import subprocess
app = Flask(__name__)
from CarDetection import *

image_name = "32.jpg"

@app.route("/")
def exec():
    # subprocess capture image if we have multiple pi & cameras
    isVacant = detect(image_name)
    return jsonify(isVacant=isVacant)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8091, debug=True)

