#Needed for the API
import requests
import json
import os 

#global variables
sprint_id = 0
active_scout_issues ={}

#setup API route/keys
base_url = "https://jira.wellspring.com/rest/"

#Scout (Starfox) Board = 94
active_sprint = "agile/1.0/board/94/sprint?state=active"

#Pulls back issues for current sprint
all_issues = "agile/1.0/board/94/sprint/"
issues = "/issue"

#Returns int of active Sprint ID
def active_sprint_id():
    global sprint_id
    response = requests.request("GET", base_url+active_sprint, headers=headers)

    #Get raw data
    active_scout_sprint = response.json()

    #Convert dict to list then get list value (probably better way to do this but this works)
    active_sprint_id = active_scout_sprint["values"]
    sprint_id = active_sprint_id[0]
    sprint_id = sprint_id["id"]

    return  sprint_id

#Returns all issues in current sprint (Needs sprint_id)
def current_scout_sprint():
    global active_scout_issues

    #Get raw data
    response = requests.request("GET", base_url+all_issues+str(sprint_id)+issues, headers=headers)
    active_scout_issues = response.json()
    
    return active_scout_issues
