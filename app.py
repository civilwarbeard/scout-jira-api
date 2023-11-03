#Flask commands -- 
#This tells flask where the app is: export FLASK_APP=app
#This tells flask to run it: flask run --debug

from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os 

app = Flask(__name__)


@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/help", methods=["GET"])
def help():
    return render_template("help.html")

@app.route("/current", methods=["GET"])
def current():
    headers = {
  'Authorization': 'Bearer OTczOTU4Mjg2ODMxOl0tPXcAsFVOeiUT6NUs8muGJk13'
  }

    #setup API route/keys
    base_url = "https://jira.wellspring.com/rest/"

    #Scout (Starfox) Board = 94
    active_sprint = "agile/1.0/board/94/sprint?state=active"

    #Pulls back issues for current sprint
    all_issues = "agile/1.0/board/94/sprint/"
    issues = "/issue"
    response = requests.request("GET", base_url+active_sprint, headers=headers)

    #Get raw data
    active_scout_sprint = response.json()

    #get sprint id from json response
    sprint_id = active_scout_sprint["values"][0]["id"]
    
    #Get raw data
    response = requests.request("GET", base_url+all_issues+str(sprint_id)+issues, headers=headers)
    active_scout_issues = response.json()
    list_of_issues = active_scout_issues["issues"]

    ##Sprint Totals
    points = []
    for item in active_scout_issues["issues"]:
        points.append(item["fields"]["customfield_10106"])

    total_points = sum(points)

    #Filters for Columns
    maintenance_issues = filter(lambda x: "Maintenance" in x["fields"]["labels"], active_scout_issues["issues"])
    mr_index_issues = filter(lambda x: "MrIndex" in x["fields"]["labels"], active_scout_issues["issues"])
    client_issues = filter(lambda x: "Client" in x["fields"]["labels"], active_scout_issues["issues"])
    project_issues = filter(lambda x: "project" in x["fields"]["labels"], active_scout_issues["issues"])
    
    return render_template("current.html",
        list_of_issues = list_of_issues,
        maintenance_issues = maintenance_issues,
        mr_index_issues = mr_index_issues,
        client_issues = client_issues,
        project_issues = project_issues,
        total_points = total_points)
