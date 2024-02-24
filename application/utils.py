import os,requests,openai
import random,string
from coda_project.settings import SITEURL
# import tableauserverclient as TSC
import datetime
from datetime import datetime as date_obj
from django.utils.text import slugify
from django import template
from django.apps import apps
from django.db.models import Q
#from langchain.agents import create_sql_agent
#from langchain_community.agent_toolkits import SQLDatabaseToolkit
#from langchain.agents.agent_types import AgentType
#from langchain_openai import ChatOpenAI, OpenAI
#from langchain_community.utilities import SQLDatabase


def generate_chatbot_response(user_message, user_message_dict=None):
    
    if user_message_dict is None:
        messages = [
        {"role": "system", "content": user_message},
        ]
    else:
        messages = user_message_dict

    client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    response = client.chat.completions.create(
    # response = openai.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            # response_format="json"
            # temperature=0.4,
            # max_tokens=4096,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0
    )
    
    if response:
        result=response.choices[0].message.content     
        
    else:
        result = None
    return result


def analyze_website_for_wcag_compliance(wcag_standards):
    wcag_standards_summary = "\n".join([
        f"{ws.criteria}: {ws.definition} What to test: {ws.what_to_test}" 
        for ws in wcag_standards
    ])

    # Construct the prompt for OpenAI
    user_message = f"Based on the following WCAG Standards, examine the CODA website to check for areas that do not meet these standards:\n\n{wcag_standards_summary}\n\nExamine the website and suggest improvements:"

    try:
        suggestions = generate_chatbot_response(user_message)
        # suggestions = openai_response.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred while contacting the OpenAI API: {e}")
        suggestions = "Could not generate suggestions due to an error."

    # You would typically return a Django HTTP response object
    # For demonstration purposes, we'll just print the suggestions
    print(suggestions)
    return suggestions

# Interview description data
posts = [
    {
        "Inteview": "First   Interview",
        "Concentration": "Data Analysis",
        "Description": "Understanding SQL,Tableau & Alteryx	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Second Interview",
        "Concentration": "General Tools& Company Projects",
        "Description": "Understanding Company Projects, Values & Systems	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Final Interview",
        "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Measuring,assessing Time sensitivity.",
        "Duration": "7 Days",
        "Lead": "Scrum Master",
    },
]

alteryx_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing Alteryx",
        "link": "https://docs.google.com/presentation/d/1sTflaF0yS8nYS4Trm9gx0H4HPH0zN7qBu9O27-vMN7A/edit#slide=id.p1",
    },
    {
        "topic": "DAF DATA CLEANING",
        "description": "DAF data cleaning workflow",
        "link": "https://transcripts.gotomeeting.com/#/s/ff2b23e11fadead1e6b4265b043f75ec8300a82d9576d7e6f79ae22568733740",
    },
    {
        "topic": "WHATSAAP MESSAGES",
        "description": "Cleaning Messages",
        "link": "https://transcripts.gotomeeting.com/#/s/8085611d7f07db4434d786635018273ad915c01230fd33202f660fe4c1fd62d5",
    },
    {
        "topic": "ALTERYX PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/1v68aYsEXskx0Ze6CEbM9k8HLjMlgHY5ZOOScsGO7j54/edit#slide=id.p1",
    },
]

dba_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing SQL Database",
        "link": "https://drive.google.com/file/d/148J8xhikG5CqroObDjUtNC3r7vk9HmxF/view?usp=drivesdk",
    },
    {
        "topic": "End to End-SQL",
        "description": "Normalization, Creation and Retrieval of Data",
        "link": "https://transcripts.gotomeeting.com/#/s/ee09457a8bec84b6e27fd0a24bb8e2bdf9186c30b88a1ef48171b2f443e61635",
    },
    {
        "topic": "SQL PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/13IQKwFjkkxJckPQWG-Q1ydZPv6tDfhpWUOt6j9mNgvQ/edit",
    },
]

tableau_list = [
    {
        "topic": "INSTALLATION",
        "description": "Installing Tableau",
        "link": "https://www.youtube.com/watch?v=QYnkudCxbmE",
    },
    {
        "topic": "Reporting",
        "description": "Developing an Executive Overview Report",
        "link": "https://drive.google.com/file/d/1yQBiDgt3y1faTfglDtVITEEnyyYIewui/view",
    },
    {
        "topic": "Tableau PPT",
        "description": "Use the powerpoint to follow along, you will use the same ppt in presenting your work",
        "link": "https://docs.google.com/presentation/d/1ASZkzSJBSoOqH6R83ZznChL6ISi5SC5_YI5N2XTZD1w/edit?usp=sharing",
    },
]


# ==============================INTERVIEW DESCRIPTION MODELS=======================================

# Interview description data

TaskInfos = [
    {
        "Inteview": "First   Interview",
        "Concentration": "Data Analysis",
        "Description": "Understanding SQL,Tableau & Alteryx	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Second Interview",
        "Concentration": "General Tools& Company Projects",
        "Description": "Understanding Company Projects, Values & Systems	",
        "Duration": "5 Days	",
        "Lead": "HR Manager",
    },
    {
        "Inteview": "Final Interview",
        "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Measuring,assessing Time sensitivity.",
        "Duration": "7 Days",
        "Lead": "Scrum Master",
    },
]
def rewardpoints(form):
    total_points = 0
    if form.cleaned_data.get('projectDescription'):
        total_points += 2
    if form.cleaned_data.get('requirementsAnalysis'):
        total_points += 3
    if form.cleaned_data.get('development'):
        total_points += 5
    if form.cleaned_data.get('testing'):
        total_points += 3
    if form.cleaned_data.get('deployment'):
        total_points += 2
    return total_points