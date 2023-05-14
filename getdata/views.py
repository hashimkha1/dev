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
    FormView,
    DetailView,
    UpdateView
)
from main.utils import Finance,Data,Management,Automation,Stocks,General
from getdata.utils import (
                    get_gmail_service,
                    search_messages,
                    get_message,
                    getdata,
                    GetSubject,
                    get_crypto_price,
                    get_stock_price,
                    row_value

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
from .models import CashappMail,ReplyMail,Editable,Logs
from investing.models import stockmarket,ShortPut,covered_calls,cread_spread,cryptomarket
from django.contrib.auth import get_user_model

from .forms import CsvImportForm
from coda_project.settings import EMAIL_INFO

putsrow_value,callsrow_value,id_value=row_value()

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


class CashappMailDetailSlugView(DetailView):
    queryset = CashappMail.objects.all()
    template_name = "getdata/detail.html"
 
    def get_context_data(self, *args, **kwargs):
        context = super(CashappMailDetailSlugView, self).get_context_data(*args, **kwargs)
        return context
 
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
 
        #instance = get_object_or_404(CashappMail, slug=slug, active=True)
        try:
            instance = CashappMail.objects.get(slug=slug, active=True)
        except CashappMail.DoesNotExist:
            raise Http404("Not found..")
        except CashappMail.MultipleObjectsReturned:
            qs = CashappMail.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance

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
    # Call the main_shortput function to retrieve the data
    message = 'we are done processing your request'
    data = main_shortput(request)
    # Loop through the data and insert it into the database
    created_count = 0
    for row in data:
        symbol = row[0]
        action = row[1]
        expiry = row[2]
        days_to_expiry = row[3]
        strike_price = row[4]
        mid_price = row[5]
        bid_price = row[6]
        ask_price = row[7]
        implied_volatility_rank = row[8]
        earnings_date = row[9]
        stock_price = row[11]
        raw_return = row[12]
        annualized_return = row[13]
        distance_to_strike = row[14]

        obj, created = ShortPut.objects.get_or_create(
            Symbol=symbol,
            Action=action,
            Expiry=expiry,
            Days_To_Expiry=days_to_expiry,
            Strike_Price=strike_price,
            defaults={
                'Mid_Price': mid_price,
                'Bid_Price': bid_price,
                'Ask_Price': ask_price,
                'Implied_Volatility_Rank': implied_volatility_rank,
                'Earnings_Date': earnings_date,
                'Stock_Price': stock_price,
                'Raw_Return': raw_return,
                'Annualized_Return': annualized_return,
                'Distance_To_Strike': distance_to_strike
            }
        )
        if created:
            created_count += 1
    # return render (request, "main/snippets_templates/output_snippets/option_data.html", context)
    return redirect ('getdata:shortputdata')

def shortputdata(request):
    message=f'we are done processing your request'
    # Retrieve the data from the database
    data = ShortPut.objects.all()
    putsrow_value,callsrow_value,id_value=row_value()
    context={
        "data":data,
        "putsrow_value":putsrow_value,
        "callsrow_value":callsrow_value,
        "id_value":id_value,
        # 'new_rows': created_count,
        # "duplicate_rows" :len(data) - created_count,
        'title': 'Success',
    }
    # Pass the data to the template
    return render (request, "main/snippets_templates/output_snippets/option_data.html", context)

# def covered_callsdata(request):
#     message=f'we are done processing your request'
#     # Retrieve the data from the database
#     data = covered_calls.objects.all()
#     print(data)
#     putsrow_value,callsrow_value,id_value=row_value()
#     context={
#         "data":data,
#         "putsrow_value":putsrow_value,
#         "callsrow_value":callsrow_value,
#         "id_value":id_value,
#         # 'new_rows': created_count,
#         # "duplicate_rows" :len(data) - created_count,
#         'title': 'Success',
#     }
#     # Pass the data to the template
#     return render (request, "main/snippets_templates/output_snippets/option_data_covered.html", context)

from django.core.paginator import Paginator

def covered_callsdata(request):
    try:
        # Retrieve the data from the database
        covered_calls_data = covered_calls.objects.all()
        print(covered_calls_data)
        # Paginate the data
        paginator = Paginator(covered_calls_data, 10)  # Display 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Get the number of rows for puts and calls
        puts_rows = len(covered_calls_data.filter(option_type='put'))
        calls_rows = len(covered_calls_data.filter(option_type='call'))

        # Get the unique IDs
        ids = covered_calls_data.order_by().values('id').distinct()

        # Render the template with the data
        context = {
            'page_obj': page_obj,
            'puts_rows': puts_rows,
            'calls_rows': calls_rows,
            'ids': ids,
            'title': 'Option Data - Covered Calls',
        }
        return render(request, 'main/snippets_templates/output_snippets/option_data_covered.html', context)

    except Exception as e:
        # Handle any errors that occur
        context = {
            'error': f'An error occurred: {e}',
            'title': 'Error',
        }
        return render(request, 'main/errors/error.html', context)

def credit_spreaddata(request):
    message=f'we are done processing your request'
    # Retrieve the data from the database
    data = cread_spread.objects.all()
    print(data)
    putsrow_value,callsrow_value,id_value=row_value()
    context={
        "data":data,
        "putsrow_value":putsrow_value,
        "callsrow_value":callsrow_value,
        "id_value":id_value,
        # 'new_rows': created_count,
        # "duplicate_rows" :len(data) - created_count,
        'title': 'Success',
    }
    # Pass the data to the template
    return render (request, "main/snippets_templates/output_snippets/option_data_credit.html", context)

class shortputupdate(UpdateView):
    model = Editable
    success_url = "/getdata/shortputdata"
    fields = "__all__"
    template_name="main/snippets_templates/generalform.html"
    if model:
        def form_valid(self, form):
            # form.instance.author=self.request.user
            return super().form_valid(form)
        def test_func(self):
            # interview = self.get_object()
            # if self.request.user.is_superuser:
                # return True
            # elif self.request.user == interview.client:
                # return True
            return True
    else:
        print("set default values")
        
    

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


def LogsViewSet(request):
    logs = Logs.objects.all().order_by("-id")
    if request.user.is_superuser:
        return render(request, "testing/logs.html", {"logs": logs})

    else:
        return redirect("main:layout")