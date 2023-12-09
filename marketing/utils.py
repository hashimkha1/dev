import os,requests
import json
import logging


logger = logging.getLogger(__name__)

def best_employee(task_obj):
    sum_of_tasks = task_obj.annotate(sum=Sum('point'))
    # logger.debug(f'sum_of_tasks: {sum_of_tasks}')
    max_point = sum_of_tasks.aggregate(max=Max('sum')).get('max')
    # logger.debug(f'max_point: {max_point}')
    best_users = tuple(sum_of_tasks.filter(sum=max_point).values_list('employee__username'))
    # logger.debug(f'best_users: {best_users}')
    return best_users


def build_message_payload(ad):
    image_url = ad.image_name.image_url
    full_image_url = f'http://drive.google.com/uc?export=view&id={image_url}'
    message = ad.message
    link = ad.link
    topic = ad.ad_title if ad.ad_title else ''
    company = ad.company if ad.company else ''
    short_name = ad.short_name if ad.short_name else ''
    signature = ad.signature if ad.signature else ''
    video_link = f"Here is the recorded video:{ad.video_link}" if ad.video_link else ''
    join_link = f"Join Zoom Meeting \n:{ad.meeting_link}" if ad.video_link else ''
    company_site = ad.company_site  # Assuming this is always present

    post = f'{company}({short_name})\n\n{topic}\n{message}\n\n.{video_link}{join_link},Questions, Please reach us: {company_site}\n{signature}'

    if image_url:
        message_type = "media"
        message_content = full_image_url
        filename = "image.jpg"
    else:
        message_type = "text"
        message_content = f'{message}\nvisit us at {link}'
        filename = None

    payload = {
        "type": message_type,
        "message": message_content,
        "text": post if message_type == "media" else None,
        "filename": filename if message_type == "media" else None
    }
    return payload

def send_message(product_id, screen_id, token, group_id, message_payload):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-maytapi-key": token,
    }
    url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(message_payload))
        if response.status_code != 200:
            logger.error(f"Error sending message to group {group_id}: {response.text}")
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")