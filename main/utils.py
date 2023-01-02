from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
from accounts.forms import UserForm
from coda_project.settings import SITEURL



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


# Interview description data

data_interview = [
    {
        "Inteview": "1. Transcripts/Speeches",
        # "Concentration": "Data Analysis",
        "Description": "Write Your Responses to all 7 questions",
        "Duration": "5 Days/3 Runs",
        "Lead": "Self/Coach",
    },
    
    {
        "Inteview": "2. Practice Sessions",
        # "Concentration": "General Tools& Company Projects",
        "Description": "Self recorded practice sessions for all 8 questions",
        "Duration": "5 Days/24 sessions",
        "Lead": "Self/Coach",
    },
    {
        "Inteview": "3. Role-Concentration",
        "Description": "Interact with a database of 80 Technical Interview Questions",
        "Duration": "5 Days	",
        "Lead": "Self/Coach",
    },
    {
        "Inteview": "4. Mock Interviews",
        # "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Real Life simulation of mock interview with coach of analytics",
        "Duration": "2 Mock/4 Past Interviews",
        "Lead": "Coach",
    },
]

Automation = [
    {
        "title": "Whatsapp",
        "link":SITEURL+"/whatsapp/",
        "linkname":"Pics&Messages-Whatsapp",
    },
    {
        "title": "Cash App",
        "link":SITEURL+"/getdata/cashappdata/",
        "linkname":"Cash app",
    },
    {
        "title": "Job Application",
        "link":SITEURL+"/getdata/replies/",
        "linkname":"Reply",
    },
    {
        "title": "To Come..",
        "link":"",
        "linkname":"To Come..",
    },
]
Stocks = [
    {
        "title": "Cryptomarket",
        "link":SITEURL+"/getdata/options/",
        "linkname":"Cryptomarket Data",
    },
    {
        "title": "Credit Spreads",
        "link":SITEURL+"/getdata/credit_spread/",
        "linkname":"Credit Spreads Data",
    },
    {
        "title": "Get short Put Data",
        "link":SITEURL+"/getdata/shortput/",
        "linkname":"Get short Put Data",
    },
    {
        "title": "Get covered Calls Data",
        "link":SITEURL+"/getdata/covered_calls/",
        "linkname":"Get covered Calls Data",
    },
]
General = [
    {
        "title": "Images/Assets",
        "link":SITEURL+"/images/",
        "linkname":"Add Images/Assets",
    },
    {
        "title": "Credit Spreads",
        "link":SITEURL+"/getdata/credit_spread/",
        "linkname":"Credit Spreads Data",
    },
    {
        "title": "Get short Put Data",
        "link":SITEURL+"/getdata/shortput/",
        "linkname":"Get short Put Data",
    },
    {
        "title": "Get covered Calls Data",
        "link":SITEURL+"/getdata/covered_calls/",
        "linkname":"Get covered Calls Data",
    },
]
Meetings = [
    {
        "title": "1-1 Session",
        "link":SITEURL+"/data/employetraining/",
        "linkname":"1-1 Session",
        "video":"#",
    },

    {
        "title": "General Meeting",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"General Meeting",
        "video":"#",

    },
    {
        "title": "BI Session",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"BI Session",
        "video":"#",
    },
    {
        "title": "SPRINT",
        "link":"https://docs.google.com/spreadsheets/u/5/d/1ILex8zOkh4Vee1dDabIadQTmmoyScaybucUiQirDfFI/edit#gid=1358242624",
        "linkname":"SPRINT",
        "video":"#",
    },
    {
        "title": "DAF SESSIONS",
        "link":"https://drive.google.com/file/d/1UsSmmJv5_83ZRegObGhgGE3C5eIJ-4E1/view",
        "linkname":"DAF",
        "video":"#",
    },
    {
        "title": "DEPARTMENT",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"departmental",
        "video":"#",
    },
    {
        "title": "BOG",
        "link":"https://docs.google.com/spreadsheets/u/5/d/1ILex8zOkh4Vee1dDabIadQTmmoyScaybucUiQirDfFI/edit#gid=1358242624",
        "linkname":"BOG",
        "video":"#",
    },
    {
        "title": "PBR",
        "link":"https://docs.google.com/spreadsheets/u/5/d/1ILex8zOkh4Vee1dDabIadQTmmoyScaybucUiQirDfFI/edit#gid=1358242624",
        "linkname":"PBR",
        "video":"#",
    },
]

# Big_data = [
#     {
#      "Automation":{
#         "title": "1. Transcripts",
#         "link": "https://www.codanalytics.net/data/iuploads/",
#     },
#     "Stocks&Options":{
#         "title": "1. Transcripts",
#         "link": "https://www.codanalytics.net/data/iuploads/",
#     },
#     }
# ]
# ==============================Apps and Models===============================
Finance = [
    {
        "title": " Transaction",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " Payment Information",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Payment History",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]
Data = [
    {
        "title": " Categrory",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " SubCategory",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Links",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]
Management = [
    {
        "title": " Task",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": " Task History",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
    {
        "title": "Other",
        "description": " Upload only a CSV File, Check field formats to minimize errors during upload.",
    },
]