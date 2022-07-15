from django.shortcuts import render
# imports added below
import json
import os

from django.shortcuts import render
from django.views.generic import ListView , DetailView , FormView
from http.client import HTTPResponse

from requests import request 
from . import forms

from django.views import View
from django.utils.dateformat import format
from django.shortcuts import redirect
import requests

import threading
import time

# top level variables declaration


dir_path = os.path.dirname(os.path.realpath(__file__))
print('---dir_path-- : ',dir_path)
urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
urlToRefresh = 'https://api.getgo.com/oauth/v2/token'
urlMeetingAttendee = "https://api.getgo.com/G2M/rest/meetings/{}/attendees"
grant_type = 'refresh_token'
refresh_token = None
client_code = None

# -----

def refresh_token_function():
    global refresh_token , client_code

    # myRefreshJSON =None
    # print('1. reading client code and refresh token')

    with open(dir_path+'/gotomeeting/credentialsForRefresh.json','r') as f:
        myJson = json.load(f)
        refresh_token = myJson['refresh_token']
        client_code = myJson['client_code']
    response = None
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic '+client_code
    }
    myPayload = "grant_type={}&refresh_token={}".format(grant_type , refresh_token)

    # print('2. making refresh token request to',urlToRefresh)

    response = requests.post(url=urlToRefresh , data=myPayload , headers=headers)
    # print('3. response-code: ',response.status_code)
    # print("4. saving new tokens in file")
    with open(dir_path+'/gotomeeting/refresh_tokens.json',"w") as f:
        f.write(response.text)
        # print("written to ",'refresh_tokens.json')
    
    # print('\n---------------done-----------------')

    ## refreshing tokens every 30 minutes
    threading.Timer(1800.0, refresh_token_function).start()
    print("--refreshing tokens at {}--".format(time.ctime()))

refresh_token_function()

# method to get meeting response from gotomeeting api


def getmeetingresponse(startDate , endDate):
    access_token = None
    print('-'*50)
    # print("1. getting access tokens")
    with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
        myJson = json.load(f)
        access_token = myJson['access_token']
    response = None
    headers = {
    'Authorization': 'Bearer '+access_token
    }
    # print("2. getting meetings from {} to {}\n".format(startDate , endDate))
    urlMeeting = urlGotoMeeting.format(''.join([str(startDate),'T12:00:00Z']) ,''.join([str(endDate),'T12:00:00Z']))
    # print("3. request made : ",urlMeeting)
    response = requests.request("GET" , url=urlMeeting , headers=headers)
    # print('4.  response-code: ',response.status_code)
    # print('5.  rendering with variable data')
    print('-'*50)
    # return [response.text]
    jsonResponse = json.loads(response.text)
    myCleanResponse = []
    for meeting in jsonResponse:
        temp = {}
        meetingItems = meeting.items()
        temp.update(meetingItems)
        if 'recording' in temp.keys():
            temp['recording'] = temp['recording']['shareUrl']
            # print('added rec link')
        else:
            temp['recording'] = "No recording"

        temp['startTime'] = temp['startTime'].replace('T',' ')
        temp['endTime'] = temp['endTime'].replace('T',' ')

        temp['startTime'] = temp['startTime'].replace('.+0000','')
        temp['endTime'] = temp['endTime'].replace('.+0000','')
        myCleanResponse.append(temp)

    return myCleanResponse





# views on ratings data.
def getrating(request):
    return render(request, 'getdata/getrating.html', {'title': 'getrating'})

def index(request):
    return render(request, 'getdata/index.html', {'title': 'index'})

def show(request):  
    employees = Employee.objects.all()  
    return render(request,"accounts/show.html",{'employees':employees})  


''' for gotomeeting data '''
# starts here ----------

def meetingFormView(request):
    # testing purpose hardcoding allDataJsons
    allDataJsons = []
    # print('1->',request.POST)
    # print('2->',request.POST.mycity)
    if request.method=='POST':
        print('here')
        print('1->',request.POST)
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        # print('2->',request.POST['startDate'])
        # print('3->',request.POST['endDate'])
        allDataJsons = []
        # filePath = dir_path+"/gotomeeting/meetings_2.json"
        allDataJsons = getmeetingresponse(startDate , endDate)
        result = {
            'data' : allDataJsons,
            'message' : "meetings between {} and {}".format( startDate , endDate)
        }
        # print('5-> result : ',result)

        return render(request, 'getdata/meetingList.html',result) #returns the index.html template

    return render(request, 'getdata/meetingForm.html') #returns the index.html template

def gotomeetingresult(request):
    print('you are here at ',request.path)
    # print('result - \n',result)
    return render(request, 'getdata/meetingList.html') #returns the index.html template


# ends here --------

## additions to view gotomeeting meeting in detail

# meetingView6
def meetingView6(request,meeting_id):
    print("\n\n view6 : you have request meeting details for path  : ",request.path)
    mID = int(meeting_id)
    with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
        myJson = json.load(f)
        access_token = myJson['access_token']
    strResponse = None
    headers = {
    'Authorization': 'Bearer '+access_token
    }
    meeting = urlMeetingAttendee.format(mID)
    print(f"fetching meeting {mID} details ->> {meeting} ")

    responseMeeting = requests.get(url=meeting,headers=headers)
    jsonResp = json.loads(responseMeeting.text)
    # print("-->> foo : ",foo)
    template_name = 'getdata/meetingDetails.html'
    # context_object_name = 'result'
    result = {"data":'meeting details id = {}'.format(meeting_id)}
    # myQuerySet = meetingView3.get_queryset()
    # {{ request.GET.urlencode }}
    cleanResponse = []
    for meeting in jsonResp:
        temp = {}
        meetingItems = meeting.items()
        temp.update(meetingItems)
        temp['joinTime'] = temp['joinTime'].replace('T',' ')
        temp['leaveTime'] = temp['leaveTime'].replace('T',' ')

        cleanResponse.append(temp)

    result['info'] = cleanResponse

    return render(request , template_name , result)
