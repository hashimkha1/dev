# import pywhatkit as pwk
# from time import sleep
from datetime import date, datetime, timedelta
import calendar,string


# import random
# from .models import FeaturedActivity,FeaturedSubCategory

import requests
def live_currency():
    # Where USD is the base currency you want to use
    url = 'https://v6.exchangerate-api.com/v6/336ccxxxxxxxxx8e74eac/latest/USD'

    # Making our request
    response = requests.get(url)
    data = response.json()

    # Your JSON object
    print(data)
    return data

# def training_response():
#     # Article.objects.filter(publications=1)
#     acts=FeaturedActivity.objects.filter(featuredsubcategory=1)
#     subs=FeaturedSubCategory.objects.filter(featuredcategory_id=1)
#     for sub in subs :
#         if sub in ["Introduction","Organization"]:
#             print(sub)

    # Publication.objects.filter(article__id=1)

    # value=request.path.split("/")
    # # newvalue=random.sample(value, 1)
    # # print(newvalue)
    # path_values = [i for i in value if i.strip()]
    # sub_title=path_values[-1]
    # # print(sub_title)
    # for activity in tasks:
    #     task_name=activity.activity_name
    #     task_question=activity.guiding_question
    #     # print(task_name,task_question)
    # return sub

# def send_msg_for_group(group_id, group_msg, gh, gm, gd):
#     sleep(10)
#     pwk.sendwhatmsg_to_group(group_id, group_msg, gh, gm, gd)


# def send_img(msg_contact, img_path, img_title, send_delay):
#     pwk.sendwhats_image(msg_contact, img_path, img_title, send_delay)


# def send_msg_for_many_groups():
#     grp_id_list = []
#     content_of_msg = "Type your message here"
#     msg_hour = 0
#     msg_min = 0
#     send_delay = 10
#     img_title = "Type your image title here"
#     img_path = "Type your image path here"

#     for i in range(grp_id_list):
#         if img_path is not None:
#             send_img(grp_id_list[i], img_path, img_title, send_delay)
#         else:
#             send_msg_for_group(
#                 grp_id_list[i], content_of_msg, msg_hour, msg_min, send_delay
#             )


# class RequirementUpdateView(LoginRequiredMixin, UpdateView):
#     model = Requirement
#     success_url = "/management/activerequirements"
#     fields = [
#         "created_by",
#         "assigned_to",
#         "requestor",
#         "company",
#         "category",
#         "app",
#         "delivery_date",
#         "duration",
#         "what",
#         "why",
#         "how",
#         "doc",
#         "is_active",
#     ]
#     form = RequirementForm

#     def form_valid(self, form):
#         # form.instance.author=self.request.user
#         if self.request.user.is_superuser:
#             req_obj = Requirement.objects.get(pk=form.instance.id)
#             old_dev = req_obj.assigned_to

#             if (not get_user_model().objects.get(pk=self.request.POST["assigned_to"]) == self.request.user
#                     and not get_user_model().objects.get(pk=self.request.POST["assigned_to"]
#                                                          ) == old_dev
#             ):
#                 if self.request.is_secure():
#                     protocol = "https://"
#                 else:
#                     protocol = "http://"

#                 subject = 'Task has been reassigned on CodaTraining'
#                 old_dev_obj = get_user_model().objects.get(username=old_dev)
#                 old_dev_email = old_dev_obj.email
#                 context = {
#                     'user': old_dev,
#                     'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
#                                                                         kwargs={'pk': form.instance.id}),
#                     'req_id': req_obj.id,
#                     'delivery_date': req_obj.delivery_date,
#                 }
#                 # logger.debug(f'old_dev_email: {old_dev_email}')
#                 # logger.debug(f'context: {context}')
#                 send_email(
#                     category=old_dev_obj.category,
#                     to_email=[old_dev_email, ],
#                     subject=subject,
#                     html_template='email/requirement_reassigned.html',
#                     context=context
#                 )

#                 subject = "Task assign on CodaTraining"
#                 to = (
#                     get_user_model()
#                     .objects.get(pk=self.request.POST["assigned_to"])
#                     .email
#                 )
#                 context = {
#                     'request_what': self.request.POST['what'],
#                     'url': protocol + self.request.get_host() + reverse('management:RequirementDetail',
#                                                                         kwargs={'pk': form.instance.id}),
#                     'delivery_date': self.request.POST['delivery_date'],
#                     'user': self.request.user,
#                 }
#                 send_email(
#                     category=self.request.user.category,
#                     to_email=[to, ],
#                     subject=subject,
#                     html_template='email/RequirementUpdateView.html',
#                     context=context
#                 )

#             return super().form_valid(form)
#         else:
#             return redirect("management:requirements-active")

#     def test_func(self):
#         requirement = self.get_object()
#         if self.request.user.is_superuser:
#             return True
#         elif self.request.user == requirement.created_by:
#             return True
#         return False



def target_date():
    year=date.today().year
    limit= date(
        date.today().year,
        date.today().month,
        calendar.monthrange(date.today().year, date.today().month)[-1],
    )
    context={
         "limit":limit,
         "year":year
    }
    return year,limit
# =====================picking values from url============
# def usertaskhistory(request, username=None, *args, **kwargs):
#     print('===============TESTING==================')
#     url_path=request.path.split("/")
#     new_list = [value for value in url_path if value != '']
#     username=new_list[-1]
#     employee =username

# @register.filter
# def in_list(value, the_list):
#     value = str(value)
#     return value in the_list.split(',')

# activities = ["one one one", "one one one session", "one one one sessions"]
# myactivities = ["oneoneone", "oneoneonesession", "oneoneonesessions"]
# activitiesmodified = [activity.lower().translate({ord(c): None for c in string.whitespace}) for activity in activities]
# print(activitiesmodified)


# @register.filter(name='activitieslist')
# def activitieslist(value, myactivities):
#     return True if value in myactivities else False

# VALID_USERNAME_RESPONSE='username is valid'
# IVALID_USERNAME_RESPONSE='username is ivalid'

# def forgot_pass():
#     if request.method =='POST':
#         username = request.form.get('username'):
#         token=db.generate_reset_token(username)
#         if token:
#             email(db.get_user(username),token)
#             flash(VALID_USERNAME_RESPONSE,'success')
#         else:
#             flash(IVALID_USERNAME_RESPONSE,'error')
#     return render_template('forgot.html')