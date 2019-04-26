from flask import Flask, render_template, redirect
import requests
import subprocess
app = Flask(__name__)

from CarDetection import *

image_name = "31.jpg"
map_name = "result_31.jpg" #TODO change to map 
slaves_url = ["http://0.0.0.0:8090/", "http://0.0.0.0:8091/"]
slaves_map = ["result_31.jpg", "result_32.jpg"] #TODO change to map

@app.route("/")
def home():
    templateData = {
            "status": "",
            "image": ""
            }

    return render_template('index.html', **templateData)


@app.route("/exec/")
def exec():
    #subprocess.call(['/usr/bin/python3 main.py'], shell=True)
    #status = "vacant" if detect(image_name) else "occupied"
    
    #TODO subprocess capture image

    all_occupied = True
    nearest = 0

    if detect(image_name):
        all_occupied = False
    else:
        #get result from slaves
        for i, url in enumerate(slaves_url):
            r = requests.get(url)
            if r.json()['isVacant']:
                nearest = i+1
                all_occupied = False
                map_name = slaves_map[i]
                break

    if all_occupied:
        status = "No spots available!"
        image = ""
    else:
        status = "Nearest: " + str(nearest)
        image = map_name

    
    templateData = {
            "status": status,
            "image": image
            }
    return render_template('index.html', **templateData)
    #return redirect("/")
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

