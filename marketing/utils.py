from django.db import models
import os,requests,openai
import json
import random,string
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
import datetime
from management.models import Whatsapp



def best_employee(task_obj):
    sum_of_tasks = task_obj.annotate(sum=Sum('point'))
    # logger.debug(f'sum_of_tasks: {sum_of_tasks}')
    max_point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    # logger.debug(f'max_point: {max_point}')
    best_users = tuple(sum_of_tasks.filter(sum=max_point).values_list('employee__username'))
    # logger.debug(f'best_users: {best_users}')
    return best_users


# def runwhatsapp(whatsapp):
#     # whatsapp_items = Whatsapp.objects.all()
#     # Get a list of all group IDs from the Whatsapp model
#     whatsapp_obj=whatsapp
#     print("whatsapp_items======>",whatsapp_obj)
#     best_users = tuple(whatsapp_obj.values_list('group_id'))
#     group_ids = list(whatsapp_obj.values_list('group_id', flat=True))

#     # Get the image URL and message from the first item in the Whatsapp model
#     image_url = whatsapp_obj[0].image_url
#     message = whatsapp_obj[0].message
#     product_id = whatsapp_obj[0].product_id
#     screen_id = whatsapp_obj[0].screen_id
#     token = whatsapp_obj[0].token

#     # Loop through all group IDs and send the message to each group
#     for group_id in group_ids:
#         print("Sending message to group", group_id)

#         # Set the message type to "text" or "media" depending on whether an image URL is provided
#         if image_url:
#             message_type = "media"
#             message_content = image_url
#             filename = "image.jpg"
#         else:
#             message_type = "text"
#             message_content = message
#             filename = None

#         # Set up the API request payload and headers
#         payload = {
#             "to_number": group_id,
#             "type": message_type,
#             "message": message_content,
#             "filename": filename,
#         }
        
#         headers = {
#             "Content-Type": "application/json",
#             "x-maytapi-key": token,
#         }
#         # Send the API request and print the response
#         url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
#         response = requests.post(url, headers=headers, data=json.dumps(payload))
#         # Check if the API request was successful
#         if response.status_code != 200:
#             return response
#     return response
