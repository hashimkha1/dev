
import json

from datetime import datetime
from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Max
from django.contrib import messages
from django.conf import settings
from django.db.models import Sum
from accounts.models import Transaction, Payment_History 


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
# from langchain.agents import create_sql_agent
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain.agents.agent_types import AgentType
# from langchain_openai import ChatOpenAI, OpenAI
# from langchain_community.utilities import SQLDatabase

CustomUser = get_user_model()

from django.db.models import Sum
from .models import Transaction, Payment_History  # Ensure these are the correct model imports

def fetch_and_process_financial_data():
    # Fetch and process transaction data
    transactions_data = Transaction.objects.values('category').annotate(
        total_amount=Sum('amount')
    )

    # Fetch and process payment information data
    payment_information_data = Payment_History.objects.values(
        'plan', 'payment_fees', 'down_payment', 'fee_balance'
    )

    # Process the data into a format for balance sheet calculation
    # This is where you aggregate the data to form your balance sheet components
    assets = calculate_assets(transactions_data, payment_information_data)
    liabilities = calculate_liabilities(transactions_data, payment_information_data)
    equity = calculate_equity(transactions_data, payment_information_data)

    return assets, liabilities, equity

def calculate_assets(transactions_data, payment_information_data):
    # Logic to calculate assets from transactions_data and payment_information_data
    # Example (you should replace this with your actual logic):
    total_assets = sum(t['total_amount'] for t in transactions_data)
    return total_assets

def calculate_liabilities(transactions_data, payment_information_data):
    # Logic to calculate liabilities
    # Example (replace with actual logic):
    total_liabilities = sum(p['fee_balance'] for p in payment_information_data)
    return total_liabilities

def calculate_equity(transactions_data, payment_information_data):
    # Logic to calculate equity
    # Example (replace with actual logic):
    total_equity = sum(p['down_payment'] for p in payment_information_data)
    return total_equity


# def fetch_and_process_financial_data(request):
#     # Fetch and process transaction data
#     transactions_data = Transaction.objects.values('category').annotate(
#         total_amount=Sum('amount')
#     )

#     # Fetch and process payment information data
#     payment_information_data = Payment_History.objects.values(
#         'plan', 'payment_fees', 'down_payment', 'fee_balance'
#     )

#     # Process the data into the format expected by OpenAI
#     transactions_summary = "\n".join([f"{t['category']}: {t['total_amount']}" for t in transactions_data])
#     payment_information_summary = "\n".join([f"Plan {p['plan']} - Fees: {p['payment_fees']}, Down Payment: {p['down_payment']}, Balance: {p['fee_balance']}" for p in payment_information_data])

#     print(transactions_summary,payment_information_summary)

#     # Construct the prompt for OpenAI
#     prompt = f"Based on the following transaction and payment information data, generate a balance sheet summary.\n\nTransactions:\n{transactions_summary}\n\nPayment Information:\n{payment_information_summary}\n\nGenerate balance sheet:"

#     # Send the prompt to OpenAI (replace with actual OpenAI call)
#     try:
#         openai_response = generate_chatbot_response(prompt)
        
#         data_dict = json.loads(openai_response)  # Assuming 'generate_chatbot_response' returns a JSON string

#         # Extract the balance sheet data from the response
#         assets = data_dict.get("assets", [])
#         liabilities = data_dict.get("liabilities", [])
#         equity = data_dict.get("equity", [])
#     except json.JSONDecodeError as e:
#         # Handle JSON parsing error
#         print(f"Error processing OpenAI response: {e}")
#         assets, liabilities, equity = [], [], []
#     except Exception as e:
#         # Handle other exceptions
#         print(f"An unexpected error occurred: {e}")
#         assets, liabilities, equity = [], [], []

#     # You would typically return a Django HTTP response object
#     # For demonstration purposes, we'll return the parsed data
#     return assets, liabilities, equity

""" ========This code is for save images in google drive======= """
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload 
from googleapiclient.discovery import build
import httplib2  # Import the httplib2 library for setting the timeout
from google.auth import exceptions
from django.contrib.auth.decorators import login_required

""" ========End of Code======== """

register = template.Library()

@register.filter
def convert_date(date_string):
    return datetime.strptime(date_string, "%m/%d/%Y").date()

def random_string_generator(size=25, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def dates_functionality():
    current_year = date_obj.now().year
    current_date = date_obj.now()
    start_of_year = date_obj(current_date.year, 1, 1)  # January 1 of the current year
    ytd_duration = (current_date - start_of_year).days
    return ytd_duration,current_year

"""======= Google Drive Code ========"""

def upload_image_to_drive(image_path, folder_id,image_name):
    
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    # SERVICE_ACCOUNT_FILE = 'main/google_drive_credetials/google_credentials.json'
    SERVICE_ACCOUNT_FILE = 'gapi/creds/google_credentials.json'

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)
    http = httplib2.Http(timeout=30) 

    file_metadata = {
        'name': image_name,
        'parents': [folder_id],  # Optional: To save the image in a specific folder.
    }

    media = MediaFileUpload(image_path, mimetype='image/jpeg')

    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f'Image ID: {file.get("id")}')

"""========End of Code======="""

# def tableau_refresh():
#     # Set Tableau Server credentials and site
#     tableau_auth = TSC.TableauAuth('USERNAME', 'PASSWORD', site_id='SITE_NAME')
#     server = TSC.Server('https://YOUR_TABLEAU_SERVER')

#     with server.auth.sign_in(tableau_auth):
#         # Get all the jobs on the site
#         all_jobs, pagination_item = server.jobs.get()

#         for job in all_jobs:
#             # Filter out only the 'Extract' type jobs
#             if job.type == 'Extract':
#                 print(f"Job ID: {job.id}, Job Type: {job.type}, Status: {job.status}, Created: {job.created_at}")



def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.title)
        except:
            slug = slugify(instance.name)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=10)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


""" =============open_ai chat bot===========   """
def generate_chatbot_response(user_message, user_message_dict=None):
    
    if user_message_dict is None:
        messages = [
        {"role": "system", "content": user_message},
        ]
    else:
        messages = user_message_dict

    client = openai.OpenAI(api_key='s7jAaRvh3kzo4bBUKSnxT3BlbkFJ6BkXWufUOsCtKGqODHzJ')

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


def parse_user_query(user_query):
    words = user_query.split()
    keywords = words
    return keywords


def generate_database_response(user_message, app='investing', table='investments'):

    # Parse the user query to extract the table and keywords
    keywords = parse_user_query(user_message)
    # Get all the models from the specified app
    app_config = apps.get_app_config(app)
    models = app_config.get_models()
    response_data = []
    # Flag to check if any matching records were found
    records_found = False

    # Define fields outside the loop
    fields = None

    # Iterate over models from the specified app
    for model in models:
        model_name = model.__name__
        # print(model_name)
        # Check if the model name matches the specified table
        if model_name.lower() == table.lower():
            fields = model._meta.get_fields()
            # print("======",model_name)
            # Process the fields for the matched model here
            model_data = []
            # for field in fields:
            #     if field.get_internal_type() == 'CharField':
            #         query = Q(**{f"{field.name}__icontains": user_message})
            #         if query:
            #             results = model.objects.filter(query)
            #             model_data.extend(results.values())

            for keyword in keywords:
                for field in fields:
                    if field.get_internal_type() == 'CharField':
                        query = Q(**{f"{field.name}__icontains": keyword})
                        if query:
                            results = model.objects.filter(query)
                            model_data.extend(results.values())

            # Append the model data if it's not empty
            if model_data:
                response_data.append({model_name: model_data})
                records_found = True

    # Add a message if no matching records were found
    if not records_found:
        table_description = {
            "Table": table,
            "Description": "This table contains information about...",
            "Fields": [field.name for field in fields if field.get_internal_type() == 'CharField']
        }
        response_data.append(table_description)
    # print("response_data=================>",response_data)
    return response_data


""" ===========End of code============ """

def buildmodel(question):
    #fetching api key 
    # https://platform.openai.com/account/api-keys
    # 
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    #Building engine
    try:
        response = openai.completions.create(
            model="text-davinci-001",
            prompt=question,
            temperature=0.4,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # res = response["choices"][0]
        # result=res['text']
        res = response.choices[0]
        result=res.text
    except:
        result = None
    return result


def analyze_website_for_wcag_compliance(uploaded_file_content):
    user_message = f"""
        html_code:{uploaded_file_content}   
        """ + """
            Please review the provided HTML code with respect to WCAG criteria. Identify specific areas in the code that do not meet the standards, and provide a rewritten, corrected version of the HTML code.
            The output should be formatted in JSON as follows:
            {
                "list_of_problems": [
                    {
                        "problem_title": "Title of Problem",
                        "description": "Description of the problem found in the page."
                    }
                ],
                "improved_code": "Corrected HTML code"
            }
            Ensure that you do not alter the key names and do not include any additional strings in the output.
    """
    try:
        suggestions =generate_chatbot_response(user_message)
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred while contacting the OpenAI API: {e}")
        suggestions = "Could not generate suggestions due to an error."
    return suggestions

def handle_openai_api_exception(responses):
    user_message = f"Consider this response {responses}. Please display the information in tabular format with fields as (list_of_problems, problem_title, description). For improved_code value, format it in proper HTML."
    try:
        return generate_chatbot_response(user_message)
    except Exception as e:
        print(f"An error occurred while contacting the OpenAI API: {e}")
        return "Could not generate suggestions due to an error."


def countdown_in_month():
    now = datetime.datetime.now()
    next_month = now.replace(day=28) + datetime.timedelta(days=4)
    next_month = next_month.replace(day=1)

    remaining_time = next_month - now
    remaining_days = remaining_time.days
    remaining_seconds = remaining_time.total_seconds()
    remaining_minutes = remaining_seconds / 60
    remaining_hours = remaining_minutes / 60
    return (
                remaining_days,
                remaining_seconds ,
                remaining_minutes ,
                remaining_hours 
            )

def path_values(request):
    try:
        previous_path = request.META.get('HTTP_REFERER', '')
    except Exception as e:
        previous_path = f"{SITEURL}/management/companyagenda/"

    pre_value = previous_path.split("/")
    previous_path_values = [i for i in pre_value if i.strip()]
    pre_sub_title = previous_path_values[-1] if previous_path_values else ""

    current_value = request.path.split("/")
    path_values = [i for i in current_value if i.strip()]
    sub_title = path_values[-1]

    return path_values, sub_title, pre_sub_title

#===============Downloading Image==================
def download_image(url):
    # Path definition
    image_path = "media/data/image.jpg"
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(res.content)
        # print("Image sucessfully Downloaded: ", image_path)
    else:
        print("Image Couldn't be retrieved")
    return image_path



def service_instances(service_shown, sub_title):
    service_category_slug = next((x.slug for x in service_shown if sub_title == x.slug), None)
    service_category_title = next((x.title for x in service_shown if sub_title == x.slug), None)
    service_description = next((x.description for x in service_shown if sub_title == x.slug), None)
    service_sub_titles = next((x.sub_titles for x in service_shown if sub_title == x.slug), None)
    service_id = next((x.id for x in service_shown if sub_title == x.slug), None)

    return (
        service_category_slug,
        service_category_title,
        service_description,
        service_sub_titles,  # Include sub_title in the returned tuple
        service_id
    )


def service_plan_instances(service_categories,sub_title):
    category_slug = next((x.slug for x in service_categories if sub_title == x.slug), None)
    category_name = next((x.name for x in service_categories if sub_title == x.slug), None)
    category_id = next((x.id for x in service_categories if sub_title == x.slug), None)
    return (category_slug,category_name,category_id)

#import pdfkit

# def convert_html_to_pdf():
#     html="main/doc_templates/appointment_letter.html"
#     html_str=str(html)
#     pdfkit.from_string(html_str, 'appointment_letter.pdf')
#     print("success")

# def convert_html_to_pdf():
#     html_path = "main/doc_templates/appointment_letter.html"
#     pdf_path = "appointment_letter.pdf"
#     pdfkit.from_file(html_path, pdf_path)
#     print("Success: HTML converted to PDF.")

# def convert_html_to_pdf(request):
#     html_path = "main/doc_templates/letter.html"
#     pdf_path = "appointment_letter.pdf"
#     pdfkit.from_file(html_path, pdf_path)
#     with open(pdf_path, 'rb') as pdf_file:
#         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="appointment_letter.pdf"'
#         return response

def split_sentences(description):
    # Split the description into separate sentences
    sentences = description.split('. ')
    # Initialize lists to store the separate descriptions
    onboarding_description = ""
    troubleshooting_description = ""
    requirement_description = ""

    # Iterate through the sentences and categorize them
    for sentence in sentences:
        if "Onboarding" in sentence:
            onboarding_description = sentence
        elif "Troubleshooting" in sentence:
            troubleshooting_description = sentence
        else:
            requirement_description = sentence
    return onboarding_description,troubleshooting_description,requirement_description

def langchainModelForAnswer(question): 

    try:
        agent_executor = create_sql_agent(
            llm=ChatOpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY'), model=os.getenv('SEACH_DATA_AI_MODEL')),
            toolkit=SQLDatabaseToolkit(
                db=SQLDatabase.from_uri(os.getenv('SOURCE_DATABASE_URI'), ignore_tables = None),
                llm=OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY'))
            ),
            verbose=False,
            agent_type=AgentType.OPENAI_FUNCTIONS
        )
        params ={
            'input': question,
        }
        response = agent_executor.invoke(params)['output']
    except Exception as e:
        print(e)
        response = "some error were there, try again!"
    return response
