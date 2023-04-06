# imports added below
import os
import time
import json
import requests
import threading
from selenium import webdriver
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime,date
from django.http import HttpResponseRedirect, Http404, JsonResponse,HttpResponse
from django.views import View
from django.utils.dateformat import format
from django.contrib import admin, messages
from django.urls import path, reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from webdriver_manager.chrome import ChromeDriverManager
from django.views.generic import (
	ListView,
    FormView
)
from main.utils import Finance,Data,Management,Automation,Stocks,General
from getdata.utils import (
                    get_gmail_service,
                    search_messages,
                    get_message,
                    getdata,
                    GetSubject,
                    get_crypto_price,
                    get_stock_price

)
from finance.models import (
        Transaction
	)

#importing Options play funcationality
from getdata.utils import(
    main_covered_calls,
    main_cread_spread,
    main_shortput
)
from .models import CashappMail,ReplyMail
from investing.models import stockmarket,ShortPut,covered_calls,cread_spread,cryptomarket
from django.contrib.auth import get_user_model

from .forms import CsvImportForm
from coda_project.settings import EMAIL_INFO

# User=settings.AUTH_USER_MODEL
User = get_user_model()
__smtp_user = EMAIL_INFO


# top level variables declaration
# views on ratings data.
def getrating(request):
    return render(request, 'getdata/getrating.html', {'title': 'getrating'})

def index(request):
    return render(request, 'getdata/index.html', {'title': 'index'})

def uploaddata(request):  
    # context = {"posts": posts}
    context = {
        "Finance": Finance,
        "Data": Data,
        "Management": Management,
    }
    return render(request,"getdata/uploaddata.html", context) 

@login_required
def bigdata(request):
    context={
        "title": "data",
        "Automation":Automation,
        "Stocks":Stocks,
        "General":General,
    }
    return render(request, "getdata/bigdata.html",context)



# ========================. DISPLAY/LIST VIEWS============================
# class CashappListView(ListView):
#     queryset = CashappMail.objects.all()
#     template_name = "main/snippets_templates/interview_snippets/result.html"

class CashappListView(ListView):
	model = CashappMail
	template_name = "main/snippets_templates/interview_snippets/result.html"
	context_object_name = "cashappdata"


# # ==================GOTOMEETING===========================
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print('---dir_path-- : ',dir_path)
# urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
# urlToRefresh = 'https://api.getgo.com/oauth/v2/token'
# urlMeetingAttendee = "https://api.getgo.com/G2M/rest/meetings/{}/attendees"
# grant_type = 'refresh_token'
# refresh_token = None
# client_code = None

# # -----

def refresh_token_function(request):
    global refresh_token , client_code

    # myRefreshJSON =None
    # print('1. reading client code and refresh token')


    # to get the current working directory
    dir_path = str(os.getcwd())
    print(dir_path)

    with open(dir_path+'/getdata/gotomeeting/credentialsForRefresh.json','r') as f:
        myJson = json.load(f)
        print("json------------------------myjson", myJson)
        refresh_token = myJson['refresh_token']
        client_code = myJson['client_code']
    response = None
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic '+client_code
    }

    myPayload = "grant_type={}&refresh_token={}".format('refresh_token' , refresh_token)

    # print('2. making refresh token request to',urlToRefresh)
    response = requests.post(url='https://authentication.logmeininc.com/oauth/token' , data=myPayload , headers=headers)
    # print('3. response-code: ',response.status_code)
    # print("4. saving new tokens in file")
    with open(dir_path+'/getdata/gotomeeting/refresh_tokens.json',"w") as f:
        f.write(response.text)
        # print("written to ",'refresh_tokens.json')
    
    # print('\n---------------done-----------------')



    ## refreshing tokens every 30 minutes
    # threading.Timer(1800.0, refresh_token_function).start()
    # print("--refreshing tokens at {}--".format(time.ctime()))

    return HttpResponse("token saved successfully")



# def getmeetingresponse(startDate , endDate):
def getmeetingresponse(startDate , endDate):
    access_token = None
    startDateTime="{}T00:00:00Z".format(startDate)
    endDateTime="{}T23:59:00Z".format(endDate)
    print('-'*50)
    dir_path = str(os.getcwd())
    print(dir_path)
    # print("1. getting access tokens")
    with open(dir_path+'/getdata/gotomeeting/refresh_tokens.json','r') as f:
        myJson = json.load(f)
        access_token = myJson['access_token']
    response = None
    headers = {
    'Authorization': 'Bearer '+access_token
    }
    urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
    # print("2. getting meetings from {} to {}\n".format(startDate , endDate))
    from datetime import datetime
    from pytz import utc
    print(startDate,endDate)
    urlMeeting = urlGotoMeeting.format(startDateTime,endDateTime)
    print("----->urll meeting",urlMeeting)

    # print("3. request made : ",urlMeeting)
    response = requests.request("GET" , url=urlMeeting , headers=headers)
    # print('4.  response-code: ',response.status_code)
    # print('5.  rendering with variable data')
    print('-'*50)
    jsonResponse = json.loads(response.text)
    myCleanResponse = []
    for meeting in jsonResponse:
        # print("meetings============>",meeting)
        temp = {}
        meetingItems = meeting.items()
        temp.update(meetingItems)
        if 'recording' in temp.keys():
            temp['recording'] = temp.get('recording').get('shareUrl')
            # print('added rec link')
        else:
            temp['recording'] = "No recording"

        temp['startTime'] = temp.get('startTime').replace('T',' ')
        temp['endTime'] = temp.get('endTime').replace('T',' ')

        temp['startTime'] = temp.get('startTime').replace('.+0000','')
        temp['endTime'] = temp.get('endTime').replace('.+0000','')
        myCleanResponse.append(temp)
    # return HttpResponse(myCleanResponse)
    return myCleanResponse

    
# ''' for gotomeeting data '''
# # starts here ----------

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
    
    
# # ==================GOTOMEETING===========================
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print('---dir_path-- : ',dir_path)
# urlGotoMeeting = "https://api.getgo.com/G2M/rest/historicalMeetings?startDate={}&endDate={}"
# urlToRefresh = 'https://api.getgo.com/oauth/v2/token'
# urlMeetingAttendee = "https://api.getgo.com/G2M/rest/meetings/{}/attendees"
# grant_type = 'refresh_token'
# refresh_token = None
# client_code = None

# # -----

# def refresh_token_function():
#     global refresh_token , client_code

#     # myRefreshJSON =None

#     with open(dir_path+'/gotomeeting/credentialsForRefresh.json', encoding='utf-8') as f:
#         myJson = json.load(f)
#         refresh_token = myJson['refresh_token']
#         client_code = myJson['client_code']
#     response = None
#     headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Authorization': 'Basic '+client_code
#     }
#     myPayload = "grant_type={}&refresh_token={}".format(grant_type , refresh_token)

#     print('2. making refresh token request to',urlToRefresh)

#     response = requests.post(url=urlToRefresh , data=myPayload , headers=headers)
#     # print('3. response-code: ',response.status_code)
#     # print("4. saving new tokens in file")
#     with open(dir_path+'/gotomeeting/refresh_tokens.json',"w") as f:
#         f.write(response.text)
#         # print("written to ",'refresh_tokens.json')
    
#     # print('\n---------------done-----------------')

#     ## refreshing tokens every 30 minutes
#     threading.Timer(1800.0, refresh_token_function).start()
#     print("--refreshing tokens at {}--".format(time.ctime()))

# refresh_token_function()

# # method to get meeting response from gotomeeting api

# def getmeetingresponse(startDate , endDate):
#     access_token = None
#     print('-'*50)
#     print("1. getting access tokens")
#     with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
#         myJson = json.load(f)
#         access_token = myJson['access_token']
#     response = None
#     headers = {
#     'Authorization': 'Bearer '+access_token
#     }
#     print("2. getting meetings from {} to {}\n".format(startDate , endDate))
#     urlMeeting = urlGotoMeeting.format(''.join([str(startDate),'T12:00:00Z']) ,''.join([str(endDate),'T12:00:00Z']))
#     print("3. request made : ",urlMeeting)
#     response = requests.request("GET" , url=urlMeeting , headers=headers)
#     print('4.  response-code: ',response.status_code)
#     # print('5.  rendering with variable data')
#     print('-'*50)
#     # return [response.text]
#     jsonResponse = json.loads(response.text)
#     myCleanResponse = []
#     for meeting in jsonResponse:
#         temp = {}
#         meetingItems = meeting.items()
#         temp.update(meetingItems)
#         if 'recording' in temp.keys():
#             temp['recording'] = temp['recording']['shareUrl']
#             # print('added rec link')
#         else:
#             temp['recording'] = "No recording"

#         temp['startTime'] = temp['startTime'].replace('T',' ')
#         temp['endTime'] = temp['endTime'].replace('T',' ')

#         temp['startTime'] = temp['startTime'].replace('.+0000','')
#         temp['endTime'] = temp['endTime'].replace('.+0000','')
#         myCleanResponse.append(temp)

#     return myCleanResponse


# ''' for gotomeeting data '''
# # starts here ----------
# def meetingFormView(request):
#     # testing purpose hardcoding allDataJsons
#     allDataJsons = []
#     # print('1->',request.POST)
#     # print('2->',request.POST.mycity)
#     if request.method=='POST':
#         print('here')
#         print('1->',request.POST)
#         startDate = request.POST['startDate']
#         endDate = request.POST['endDate']
#         # print('2->',request.POST['startDate'])
#         # print('3->',request.POST['endDate'])
#         allDataJsons = []
#         # filePath = dir_path+"/gotomeeting/meetings_2.json"
#         allDataJsons = getmeetingresponse(startDate , endDate)
#         result = {
#             'data' : allDataJsons,
#             'message' : "meetings between {} and {}".format( startDate , endDate)
#         }
#         # print('5-> result : ',result)

#         return render(request, 'getdata/meetingList.html',result) #returns the index.html template

#     return render(request, 'getdata/meetingForm.html') #returns the index.html template

# def gotomeetingresult(request):
#     print('you are here at ',request.path)
#     # print('result - \n',result)
#     return render(request, 'getdata/meetingList.html') #returns the index.html template


# # ends here --------

# ## additions to view gotomeeting meeting in detail

# # meetingView6
# def meetingView6(request,meeting_id):
#     print("\n\n view6 : you have request meeting details for path  : ",request.path)
#     mID = int(meeting_id)
#     with open(dir_path+'/gotomeeting/refresh_tokens.json','r') as f:
#         myJson = json.load(f)
#         access_token = myJson['access_token']
#     strResponse = None
#     headers = {
#     'Authorization': 'Bearer '+access_token
#     }
#     meeting = urlMeetingAttendee.format(mID)
#     print(f"fetching meeting {mID} details ->> {meeting} ")

#     responseMeeting = requests.get(url=meeting,headers=headers)
#     jsonResp = json.loads(responseMeeting.text)
#     # print("-->> foo : ",foo)
#     template_name = 'getdata/meetingDetails.html'
#     # context_object_name = 'result'
#     result = {"data":'meeting details id = {}'.format(meeting_id)}
#     # myQuerySet = meetingView3.get_queryset()
#     # {{ request.GET.urlencode }}
#     cleanResponse = []
#     for meeting in jsonResp:
#         temp = {}
#         meetingItems = meeting.items()
#         temp.update(meetingItems)
#         temp['joinTime'] = temp['joinTime'].replace('T',' ')
#         temp['leaveTime'] = temp['leaveTime'].replace('T',' ')

#         cleanResponse.append(temp)

#     result['info'] = cleanResponse

#     return render(request , template_name , result)

# ========================================UPLOADING DATA SECTION========================


	
def get_urls(self):
    urls = super().get_urls()
    new_urls = [
        path("upload-csv/", self.upload_csv),
    ]
    return new_urls + urls

def upload_csv(request):

    if request.method == "POST":
        csv_file = request.FILES["csv_upload"]

        if not csv_file.name.endswith(".csv"):
            messages.warning(
                request, "The wrong file type was uploaded, it should be a csv file"
            )
            return render(request, "getdata/uploaddata.html")
            # return HttpResponseRedirect(request.path_info)

        # file= csv_file.read().decode("utf-8")
        file = csv_file.read().decode("ISO-8859-1")
        file_data = file.split("\n")
        csv_data = [line for line in file_data if line.strip() != ""]
        print(csv_data)
        for x in csv_data:
            fields = x.split(",")
            created = Transaction.objects.update_or_create(
                activity_date=fields[0],
                sender=fields[1],
                receiver=fields[2],
                phone=fields[3],
                qty=fields[4],
                amount=fields[5],
                payment_method=fields[6],
                department=fields[7],
                category=fields[8],
                type=fields[9],
                description=fields[10],
                receipt_link=fields[11],
            )
        url = reverse("main:layout")
        return HttpResponseRedirect(url)
    form = CsvImportForm()
    data = {"form": form}
    # return render(request, "admin/csv_upload.html", data)
    return render(request, "getdata/uploaddata.html", data)


def options(request):
    service = get_gmail_service()
    messages = search_messages(service= service, query= 'Robinhood')
    for message in messages:
        msg_id = message['id']
        print(msg_id)
        data = get_message(service=service, msg_id=msg_id)
        soup = getdata(data)
        if soup == 0:
            os.remove(data)
            continue
        try:
            subjectname = GetSubject(soup)
            if subjectname == None:
                os.remove(data)
                continue
        except:
            continue
        print(f'Order executed : {subjectname}')
        #This is for stock price
        if subjectname == 'Option Order Executed':
            get_stock_price(soup, subjectname)
            os.remove(data)
        #This is for crypto currency
        elif subjectname == 'Order Executed':
            get_crypto_price(soup, subjectname)
            os.remove(data)
        else:
            os.remove(data)
        # return render(request, "getdata/options.html")
        return redirect("getdata:stockmarket")


def options_play_covered_calls(request):
    main_covered_calls()
    message=f'we are done processing your request'
    context={
         "message":message,
         "title":"Process Done"
    }
    return render (request, "main/messages/general.html",context)

def options_play_cread_spread(request):
    main_cread_spread()
    message=f'we are done processing your request'
    context={
         "message":message,
         "title":"Process Done"
    }
    return render (request, "main/messages/general.html",context)
    

def options_play_shortput(request):
    # msg = main_shortput()
    # values=main_shortput()
    # email = __smtp_user.get("USER")
    # password = __smtp_user.get("PASS")
    # data=main_shortput(email, password)
    data=main_shortput()
    message=f'we are done processing your request'
    context={
         "message":message,
         "title":"Process Done",
        "msg": "DONE",
        "values":data
    }
    return render (request, "main/messages/general.html", context)

# def options_play_shortput(request):
#     # msg = main_shortput()
#     # values=main_shortput()
#     email = __smtp_user.get("USER")
#     password = __smtp_user.get("PASS")
#     # data=main_shortput(email, password)
#     data=main_shortput()
#     message=f'we are done processing your request'
#     context={
#          "message":message,
#          "title":"Process Done",
#         "msg": "DONE",
#         "values":data,
#     }
#     return render (request, "main/snippets_templates/output_snippets/option_data.html", context)

def options_play_shortputer(request):
    email = __smtp_user.get("USER")
    password = __smtp_user.get("PASS")
    # Call the main_shortput function to retrieve the data
    # data=main_shortput(email, password)
    data=main_shortput()
    # Loop through the data and insert it into the database
    for row in data:
        Symbol=row[0]
        Action=row[1]
        Expiry=row[2]
        Days_To_Expiry=row[3]
        Strike_Price=row[4]
        Mid_Price=row[5]
        Bid_Price=row[6]
        Ask_Price=row[7]
        Implied_Volatility_Rank=row[8]
        Earnings_Date=row[9]
        Earnings_Flag =row[10]
        Stock_Price=row[11]
        Raw_Return=row[12]
        Annualized_Return=row[13]
        Distance_To_Strike =row[14]
        
        obj = ShortPut(
                       stock=stock, action=action, Days_To_Expiry=Days_To_Expiry, 
                       Strike_Price=Strike_Price, Mid_Price=Mid_Price, Bid_Price=Bid_Price, 
                       Ask_Price=Ask_Price, Implied_Volatility_Rank=Implied_Volatility_Rank, 
                       Earnings_Date=Earnings_Date, Earnings_Flag=Earnings_Flag,Stock_Price=Stock_Price,
                       Raw_Return=Raw_Return, Annualized_Return=Annualized_Return,Distance_To_Strike=Distance_To_Strike
                       )
        obj.save()

    # Retrieve the data from the database
    data = ShortPut.objects.all()

    message=f'we are done processing your request'
    context={
         "message":message,
         "title":"Process Done",
        "msg": "DONE",
        "data":data,
    }
    # Pass the data to the template
    return render (request, "main/snippets_templates/output_snippets/option_data.html", context)


class OptionList(ListView):
    model=stockmarket
    template_name="getdata/options.html"
    context_object_name = "stocks"

class OptionList(ListView):
    model=stockmarket
    template_name="getdata/options.html"
    context_object_name = "stocks"


def selinum_test(request):
    # to test on server
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


    # to test on local
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument('--no-sandbox')
    # options.add_argument("--disable-gpu")
    # ## might not be needed
    # options.add_argument("window-size=800x600")
    #
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


    # Navigate to Google's homepage
    driver.get("https://www.google.com/")

    # Get the page title
    title = driver.title
    return HttpResponse(title)


