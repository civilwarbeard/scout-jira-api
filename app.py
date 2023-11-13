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
    headers = {
  'Authorization': BEARER_TOKEN
  }

    #URLS
    #setup API route/keys
    base_url = "https://jira.wellspring.com/rest/"

    #Scout (Starfox) Board = 94
    active_sprint = "agile/1.0/board/94/sprint?state=active"
    all_issues = "agile/1.0/board/94/sprint/"
    issues = "/issue"

    #Get sprint current sprint id for issues request
    response = requests.request("GET", base_url+active_sprint, headers=headers)
    current_sprint = response.json()
    sprint_id = current_sprint["values"][0]["id"]

    response = requests.request("GET", base_url+all_issues+str(sprint_id)+issues, headers=headers)
    current_sprint_issues = response.json()
    return render_template("landing.html",
        current_sprint_issues=current_sprint_issues,
        sprint_id=sprint_id)

@app.route("/help", methods=["GET"])
def help():
    return render_template("help.html")

@app.route("/current", methods=["GET"])
def current():
    headers = {
  'Authorization': 'Bearer OTQ1MjQ3ODMwNjMxOvSONf0GauaTrb/N3FZo1KB5rM7u'
  }

    #URLS
    #setup API route/keys
    base_url = "https://jira.wellspring.com/rest/"

    #Scout (Starfox) Board = 94
    active_sprint = "agile/1.0/board/94/sprint?state=active"
    all_issues = "agile/1.0/board/94/sprint/"
    issues = "/issue"

    #Get sprint current sprint id for issues request
    response = requests.request("GET", base_url+active_sprint, headers=headers)
    current_sprint = response.json()
    sprint_id = current_sprint["values"][0]["id"]

    response = requests.request("GET", base_url+all_issues+str(sprint_id)+issues, headers=headers)
    current_sprint_issues = response.json()

    ##Sprint Totals
    points = []
    for item in current_sprint_issues["issues"]:
        points.append(item["fields"]["customfield_10106"])

    total_points = sum(points)

    #Filters for Columns   NEED TO UPDATE Filters to be accepted / not accepted AND label specific... shoudl 
    #have 6 total and maybe overall accepted
    maintenance_issues = filter(lambda x: "Maintenance" in x["fields"]["labels"], current_sprint_issues["issues"])
    mr_index_issues = filter(lambda x: "MrIndex" in x["fields"]["labels"], current_sprint_issues["issues"])
    client_issues = filter(lambda x: "Client" in x["fields"]["labels"], current_sprint_issues["issues"])
    project_issues = filter(lambda x: "project" in x["fields"]["labels"], current_sprint_issues["issues"])
    accepted_issues = filter(lambda x: "Accepted" in x["fields"]["status"]["name"], current_sprint_issues["issues"])
    accepted_client_issues = filter(lambda x: "Accepted" in x["fields"]["status"]["name"] and "Client" in x["fields"]["labels"], 
        current_sprint_issues["issues"])
    
    return render_template("current.html",
        current_sprint_issues = current_sprint_issues,
        maintenance_issues = maintenance_issues,
        mr_index_issues = mr_index_issues,
        client_issues = client_issues,
        project_issues = project_issues,
        total_points = total_points,
        accepted_issues = accepted_issues,
        accepted_client_issues = accepted_client_issues,
        sprint_id = sprint_id)
