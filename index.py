#!/usr/bin/env python3

from flask import Flask, render_template, redirect
import requests
import subprocess
app = Flask(__name__)

from CarDetection import *


map_name = "map_1.png"  # init map
slaves_url = ["http://192.168.137.46:8090/", "http://192.168.137.46:8091/", "http://192.168.137.46:8092/"]
slaves_map = ["map_1.png", "map_2.png", "map_3.png"]

@app.route("/")
def home():
    templateData = {
            "status": "",
            "image": "map.png"
            }

    return render_template('index.html', **templateData)


@app.route("/exec/")
def exec():
    map_name = "map_1.png"
    
    all_occupied = True
    nearest = 1

    
    status = ""
    image = ""
    #get result from slaves
    for i, url in enumerate(slaves_url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            if r.json()['isVacant']:
                nearest = i+1
                all_occupied = False
                map_name = slaves_map[i]
                break
        except requests.exceptions.HTTPError as err:
            print("Failed to get"+url)
            continue

    if all_occupied:
        status = "No spots available!"
        image = "map.png"
    else:
        status = "Nearest: " + str(nearest)
        image = map_name

    
    templateData = {
            "status": status,
            "image": image
            }
    return render_template('index.html', **templateData)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

