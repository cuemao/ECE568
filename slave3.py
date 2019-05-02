from flask import Flask, jsonify
import subprocess
app = Flask(__name__)
from CarDetection import *

image_name = "cam_s3.jpg"

@app.route("/")
def exec():
    # subprocess capture image if we have multiple pi & cameras
    isVacant = detect(image_name)
    return jsonify(isVacant=isVacant)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8092, debug=True)

