from flask import Flask, jsonify
import subprocess
app = Flask(__name__)
from CarDetection import *

image_name = "cam_s1.jpg"

@app.route("/")
def exec():
    # subprocess capture image if we have multiple pi & cameras
    subprocess.call(['raspistill -o images/cam_s1.jpg -n -t 10 --colfx 128:128'], shell=True)
    isVacant = detect(image_name)
    return jsonify(isVacant=isVacant)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)

