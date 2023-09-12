import os,requests,openai
import random,string
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
from accounts.forms import UserForm
from django.http import HttpResponseRedirect, Http404, JsonResponse,HttpResponse
from accounts.models import CustomerUser
from coda_project.settings import SITEURL
# import tableauserverclient as TSC
import datetime
from datetime import datetime as date_obj
from django.utils.text import slugify
# from main.models import Assets
# from yourapp.utils import random_string_generator

from django import template

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



def buildmodel(question):
    #fetching api key 
    # https://platform.openai.com/account/api-keys
    # 
    openai.api_key = os.environ.get('OPENAI_API_KEY')
   
    # print(openai.api_key)

    #Building engine
    try:
        response = openai.Completion.create(
            model="text-davinci-001",
            prompt=question,
            temperature=0.4,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        res = response["choices"][0]
        result=res['text']
    except:
        result = None
    return result

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
reviews = [
    {
        "topic": "data analyst",
        "description": "My data analyst coach was truly exceptional, surpassing my expectations in every aspect. Their expertise and dedication to guiding me through the complexities of data analysis were evident from the very beginning. They possessed an in-depth understanding of various analytical techniques, tools, and methodologies, which they skillfully imparted to me. Their teaching style was both informative and engaging, breaking down intricate concepts into easily digestible segments. Through their patient explanations and real-world examples, I gained not only theoretical knowledge but also practical insights into the field of data analysis.",
    },
    {
        "topic": "data analyst",
        "description": "What truly set my data analyst coach apart was their unwavering commitment to my learning journey. They took a personalized approach, tailoring the coaching sessions to my pace of learning and adapting to my specific learning preferences. This level of individualized attention made me feel valued as a student and boosted my confidence in tackling challenging topics. Beyond the technical aspects, my coach was a great motivator. They consistently encouraged me to explore beyond the curriculum, promoting critical thinking and independent problem-solving. Their mentorship extended beyond the coaching sessions – they were always approachable, ready to answer my questions, and provide guidance whenever I faced hurdles.",
    },
    {
        "topic": "data analyst",
        "description": "Reflecting on my experience with my data analyst coach, I can confidently say that their impact on my professional growth has been profound. Their guidance not only equipped me with the skills necessary for effective data analysis but also instilled in me a deeper appreciation for the power of data-driven decision-making. Their influence transcended the role of a coach; they became a role model. Their passion for the subject was infectious, inspiring me to push my boundaries and strive for excellence. As I continue to advance in my career as a data analyst, I carry forward the invaluable lessons and insights they imparted. I am truly grateful for the opportunity to have been mentored by such an outstanding data analyst coach.",
    },
    {
        "topic": "data analyst",
        "description": "I consider myself fortunate to have had such an outstanding data analyst coach. Their passion for the subject matter is palpable, and it resonates in their teaching. Beyond the classroom, they encourage independent thinking and provide resources that extend the learning experience beyond the curriculum. What truly sets them apart is their commitment to personalized instruction. They take the time to understand each student's strengths, weaknesses, and learning style, adapting their teaching methods accordingly. Their patience and willingness to repeat explanations or explore alternative approaches ensure that no student is left behind. The coach's mentoring extends beyond technical skills; they offer career guidance, sharing insights about the industry and potential opportunities. This holistic approach has not only refined my data analysis skills but has also prepared me for a successful career in the field.",
    },
    {
        "topic": "data analyst",
        "description": "My data analyst coach has been nothing short of exceptional throughout my learning journey. Their expertise and dedication have been instrumental in shaping my understanding of data analysis. They have a remarkable ability to simplify complex concepts, making even the most intricate aspects of data analysis accessible and understandable. Their teaching style is engaging and interactive, ensuring that I remain engaged and motivated. The coach's real-world experience in data analysis brings an added dimension to their teaching, as they are able to provide practical insights and share valuable industry examples that enrich my learning experience. Their consistent availability for questions and feedback has created a supportive learning environment where I feel comfortable seeking clarification and guidance. I can confidently say that their guidance has been pivotal in my growth as a data analyst.",
    },
]


# Interview description data

data_interview = [
    {
        "Inteview": "1. Transcripts",
        # "Concentration": "Data Analysis",
        "Description": "Write Your Responses to 8 Topics",
        "Duration": "5 Days/3 Runs",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/iuploads/",
    },
    
    {
        "Inteview": "2. Practice Sessions",
        # "Concentration": "General Tools& Company Projects",
        "Description": "Self recorded practice sessions for all 8 questions",
        "Duration": "5 Days/24 sessions",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/management/sessions",
    },
    {
        "Inteview": "3. Role-Concentration",
        "Description": "Interact with a database of 80 Technical Interview Questions",
        "Duration": "5 Days	",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/prepquestions/",
    },
    {
        "Inteview": "4. Mock Interviews",
        # "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Real Life simulation of mock interview with coach of analytics",
        "Duration": "2 Mock/4 Past Interviews",
        "Lead": "Coach",
        "Link": "https://drive.google.com/file/d/1-R6R-CyHNo6b-MIN33wYwWfsDQP1NB1L/view",
    },
    {
        "Inteview": "5. Job Application & Salary Negotiation",
        # "Concentration": "Data Analysis 1-1 Sessions",
        "Description": "Guide you on how to apply and respond to recruiters",
        "Duration": "14 Days",
        "Lead": "self/Coach",
        "Link": SITEURL+"/data/job_market/",
    },
]
job_support = [
    {
        "Inteview": "1. onboarding",
        "Description": "Organization,Working PPT",
        "Duration": "4 hours",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/iuploads/",
    },
    
    {
        "Inteview": "2. Requirements",
        "Description": "Elicitation  Questions",
        "Duration": "Ongoing",
        "Lead": "Self/Coach",
        "Link": "https://app.box.com/s/oee1wn85sk2slbc0fkzs2sahe8ob8qhi",
        # https://app.box.com/s/oee1wn85sk2slbc0fkzs2sahe8ob8qhi
    },

    {
        "Inteview": "2. Project Definition",
        "Description": "SDLC Process in Box",
        "Duration": "Ongoing",
        "Lead": "Self/Coach",
        "Link": "https://app.box.com/s/fqdxfywn8c0uixarpuvoo2o7gx18lwdw",
    },
    {
        "Inteview": "3. Technical Support",
        "Description": "Training & Troubleshooting",
        "Duration": " >25 hours",
        "Lead": "Self/Coach",
        "Link": SITEURL+"/data/Development/",
    },
]

Automation = [
    {
        "title": "Social Media",
        "link":SITEURL+"/marketing/",
        "description":"Posting ads to social media",
    },
    {
        "title": "Cash App",
        "link":SITEURL+"/getdata/cashappdata/",
        "description":"Fetching data from Cashapp and updating records",
    },
    {
        "title": "Job Application",
        "link":SITEURL+"/getdata/replies/",
        "description":"Automating Job applications",
    },

    {
        "title": "Stocks & Options",
        "link":SITEURL+"/investing/optionlist/",
        "description":"Fetching information from options play",
    },
]


Stocks = [
    {
        "title": "Cryptomarket",
        "link":SITEURL+"#",
        "linkname":"Cryptomarket Data",
    },
    {
        "title": "Credit Spreads",
        "link":SITEURL+"/investing/credit_spread/",
        "linkname":"Credit Spreads",
    },
    {
        "title": "Short Puts",
        "link":SITEURL+"/investing/shortputdata/",
        "linkname":"Short Puts",
    },
    {
        "title": "covered Calls",
        "link":SITEURL+"/investing/covered_calls/",
        "linkname":"covered Calls",
    },
]


General = [
    {
        "title": "ChatGPT",
        "link":"https://chat.openai.com/chat",
        "description":"CHATGPT",
    },
    {
        "title": "Images/Assets",
        "link":SITEURL+"/images/",
        "description":"Images and assets",
    },
    {
        "title": "Open Urls",
        "link":SITEURL+"/plan_urls/",
        "description":"Script to automate simple tasks",
    },
    {
        "title": "Testimonials",
        "link":SITEURL+"/post/new/",
        "description":"Using AI to aid Clients to leave feedback",
    },
  
]

url_mapping = {
        "development": [
            "https://chat.openai.com/",
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net",
            "https://github.com/coachofanalytics/coda",
            "https://id.heroku.com/login"
        ],
        'company': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net/management/companyagenda/",
            "https://www.codanalytics.net/accounts/clients/",
            "https://www.codanalytics.net/management/tasks/",
            "https://www.codanalytics.net/management/evidence/",
            "https://www.upwork.com/",
        ],
        'family': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.google.com",
            "https://www.example.com",
            "https://www.openai.com"
        ],
        'investment': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://new.optionsplay.com/login",
            "https://robinhood.com/",
            "https://www.bankofamerica.com/smallbusiness/",
           "https://www.codanalytics.net/investing/companyreturns/",
           "https://www.codanalytics.net/investing/overboughtsold/"
        ],
        'banking': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://wwws.betterment.com/app/login",
            "https://www.bankofamerica.com/smallbusiness/",
            "https://www.ibanking.stanbicbank.co.ke/",

        ],
        'job': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://myapp.tcs.com/logon/LogonPoint/tmindex.html",
            "https://auth.ultimatix.net/utxLogin/login",
            "https://myapp.tcs.com/logon/LogonPoint/tmindex.html",

        ],
        'health': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.ushealthgroup.com/",
            "https://book.allcarefamilymed.com/primary-care/#locations",

        ],
        'government': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.irs.gov/",
            "https://www.kra.go.ke/",
            "https://www.coinbase.com/",

        ],
        'presentations': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net/investing/companyreturns/",
            "https://www.codanalytics.net/getdata/bigdata/",
            "https://drive.google.com/drive/u/0/folders/1eetZ2UnptBQnEcPMVtWaXbOvxNoZKBHJ",
        ],
        'projects': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net/management/dyc_requirements/",
            "https://drive.google.com/drive/u/0/folders/1LQOenMtdEjRcja5A6QZjj88Zm8zwt62X",
            "https://drive.google.com/file/d/1z59h0xa7afd895f69V_ICzqdLg8wSJr1/view?usp=drive_link",
            "https://docs.google.com/document/d/10QZcGATLPU7QrOMUl-dlHb-McJ6NIvL9/edit?usp=drive_link&ouid=115037154650831613074&rtpof=true&sd=true",
            "https://docs.google.com/document/d/1kt_9tFQ267bXCf2-VdObyAoyQEnj1How/edit?rtpof=true",
            "https://drive.google.com/drive/u/0/folders/1dEhB6kaQvCsefdNa63Z2F4vOG96c1dk5",
        ],
        'training': [
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net/data/start_training/interview/",
            "https://docs.google.com/presentation/d/1uhGV-1FQZgKkOdUhG5dSFt-5c-u8rTans5xyGYtvIrg/edit#slide=id.g1",
        ],
        'interview': [
            "https://chat.openai.com/",
            "https://www.codanalytics.net/accounts/credentials/",
            "https://www.codanalytics.net/data/start_training/interview/",
            "https://drive.google.com/drive/u/0/folders/1LCK0emfU4ytpZ05Dg-ZoGFOraGc0hZ4u",
            "https://drive.google.com/drive/u/0/folders/1X-3TDBkN3-FJMYHjnaA_g-P76Yy6BgCj",
            "https://www.codanalytics.net/data/updatelist/",
            "https://app.box.com/file/345111367782",
            "https://www.codanalytics.net/finance/finance_report/",
            "https://www.codanalytics.net/getdata/bigdata/",
            "https://www.optionsplay.com/hub/short-puts",
            "https://docs.google.com/spreadsheets/d/1Ra8Kf2U80wK_Mj9hXfp9B2y2egYlG0Js/edit#gid=855436689",

        ]
    }

Meetings = [
    {
        "title": "1-1 Session",
        "link":"https://docs.google.com/presentation/d/1NkgvW-ruCwCQTlkO9af75kUdKBGF9Vem/edit#slide=id.p1",
        "linkname":"1-1 Session",
        "video":"https://drive.google.com/file/d/1g0Esp33N6xR3pn7Z9-76yYxS3m_81HWH/view?usp=share_link",
    },

    {
        "title": "General Meeting",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"General Meeting",
        "video":"https://transcripts.gotomeeting.com/#/s/085feaf847fb42db28a68d5d507b871d4bed978d767e837ad3dfb2e473a57e41",

    },
    {
        "title": "BI Session",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"BI Session",
        "video":"https://transcripts.gotomeeting.com/#/s/47f94d4d116bd8d2214eea00edc483d9289915496671f9b7c82eda5512634846",
    },
    {
        "title": "SPRINT",
        "link":"https://docs.google.com/spreadsheets/u/5/d/1ILex8zOkh4Vee1dDabIadQTmmoyScaybucUiQirDfFI/edit#gid=1358242624",
        "linkname":"SPRINT",
        "video":"https://transcripts.gotomeeting.com/#/s/1ffa25cf84e5fc1b531df945fa358990166ef871f7c7854402876d22d619bf59",
    },
    {
        "title": "DAF SESSIONS",
        "link":"https://drive.google.com/file/d/1UsSmmJv5_83ZRegObGhgGE3C5eIJ-4E1/view",
        "linkname":"DAF",
        "video":"https://transcripts.gotomeeting.com/#/s/d88210a7703467f606586da252e8cb8349de7dc74e1e4cdec2a74307131985d5",
    },
    {
        "title": "DEPARTMENT",
        "link":SITEURL+"/management/companyagenda/",
        "linkname":"departmental",
        "video":"#",
    },
    {
        "title": "BOG",
        "link":"https://docs.google.com/spreadsheets/d/1wTiUJnhzfJWCw_i5XgH531LvzDhytoLRrU0fwSij88w/edit#gid=1239081146",
        "linkname":"BOG",
        "video":"#",
    },
    {
        "title": "PBR",
        "link":"https://docs.google.com/spreadsheets/d/18D2D0jr5MRGovoDJpfTkks4JxgU32w5x/edit#gid=1089504823",
        "linkname":"PBR",
        "video":"https://drive.google.com/file/d/1hDMaa9b-sjbsHGy7n4upseNdiKnSvAL-/view?usp=sharing",
    },
]

# Big_data = [
#     {
#      "Automation":{
#         "title": "1. Transcripts",
#        "link": "SITEURL+"/data/iuploads/",
#     },
#     "Stocks&Options":{
#         "title": "1. Transcripts",
#        "link": "SITEURL+"/data/iuploads/",
#     },
#     }
# ]
# ==============================Apps and Models===============================

App_Categories = {
    "Finance": [
        {
            "table_name": "Transaction",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Payment Information",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Payment History",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        }
    ],
    "Data": [
        {
            "table_name": "Category",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "SubCategory",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Links",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        }
    ],
    "Management": [
        {
            "table_name": "Task",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Task History",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Other",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        }
    ],
    "Investing": [
        {
            "table_name": "Returns",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "OverBoughtSold",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        },
        {
            "table_name": "Other",
            "description": "Upload only a CSV File, Check field formats to minimize errors during upload."
        }
    ]
}


team_members = [
    {
        "title": "Lead Team",
        "description":"The Lead Team consists of experienced professionals who provide leadership and guidance in the analytics field. They have a deep understanding of business processes and use their expertise to drive strategic decision-making.These individuals are responsible for overseeing projects, managing teams, and ensuring the successful execution of analytics initiatives.With their strong analytical skills and extensive industry knowledge, the Lead Team plays a crucial role in delivering valuable insights and driving business growth.",
    },
    {
        "title": "Support Team",
        "description":"The Supporting Tech Team comprises skilled professionals who provide technical support and expertise to enable effective analytics operations. They work closely with the Lead Team and other stakeholders to develop and maintain the infrastructure, tools, and technologies required for data analysis and reporting. These individuals possess strong technical skills and stay up-to-date with the latest advancements in analytics technology.",
    },
    {
        "title": "Trainee Team",
        "description":"The CODA Trainee Team consists of enthusiastic individuals who are undergoing training in the field of analytics through the CODA program. The CODA program provides trainees with hands-on experience and practical knowledge in various aspects of analytics. The trainees work closely with the Lead Team and Supporting Tech Team to learn and apply analytical techniques, tools, and methodologies.",
    },

]
client_categories = [
    {
        "title": "Job Seekers",
        "description":"Experienced IT professionals actively seeking employment opportunities, including Business Analysts, Project Managers, and Data Analysts, possess valuable insights and skills that can greatly contribute to organizations across diverse domains. These professionals bring a wealth of expertise and industry knowledge, enabling them to make significant contributions to the growth and success of businesses."
    },
    {
        "title": "Job Support",
        "description":"This is a group of experienced IT Experts whom CODA has assisted in finding employment in the job market. These professionals possess diverse technical skills and contribute to various domains such as software development, systems administration, database management, and cybersecurity. Through the collaborative efforts of CODA and these experts, job seekers receive support in navigating the job market and securing rewarding career opportunities."
    },

]

def service_instances(service_shown,sub_title):
    service_category_slug = next((x.slug for x in service_shown if sub_title == x.slug), None)
    service_category_title = next((x.title for x in service_shown if sub_title == x.slug), None)
    service_description = next((x.description for x in service_shown if sub_title == x.slug), None)
    service_id = next((x.id for x in service_shown if sub_title == x.slug), None)
    return (service_category_slug,service_category_title,
            service_description,service_id)

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
