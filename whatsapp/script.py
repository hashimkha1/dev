import pywhatkit as pwk
from time import sleep
import requests
# def extract_image():
#     # download the image from the URL
#     url = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_960_720.jpg"
#     image_path = "images/image.jpg"
#     res = requests.get(url, stream=True)
#     if res.status_code == 200:
#         with open(image_path, "wb") as f:
#             f.write(res.content)
#         print("Image sucessfully Downloaded: ", image_path)
#         return image_path
#     else:
#         print("Image Couldn't be retrieved")


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
#     img_path=extract_image()
#     img_title = "Type your image title here"
#     # img_path = "Type your image path here"

#     url = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_960_720.jpg"
#     image_path = "images/image.jpg"
#     res = requests.get(url, stream=True)
#     if res.status_code == 200:
#         with open(image_path, "wb") as f:
#             f.write(res.content)
#         print("Image sucessfully Downloaded: ", image_path)
#         return image_path
#     else:
#         print("Image Couldn't be retrieved")
#     for i in range(grp_id_list):
#         if img_path is not None:
#             send_img(grp_id_list[i], img_path, img_title, send_delay)
#         else:
#             send_msg_for_group(
#                 grp_id_list[i], content_of_msg, msg_hour, msg_min, send_delay
#             )



# download the image from the URL
def whatsapp():
    # url = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_960_720.jpg"
    url = "https://www.codanalytics.net/static/main/img/service-3.jpg"
    # url = "https://drive.google.com/file/d/1YATyVows61SsGDmWF846-qApkql_323m/view?usp=share_link"
    image_path = "images/image.jpg"
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(image_path, "wb") as f:
            f.write(res.content)
        print("Image sucessfully Downloaded: ", image_path)
    else:
        print("Image Couldn't be retrieved")

    # group IDs
    group_ids = ['Dv23sZ5Ctxm9HJf2lQeFEu','I0zuqJ91GgOFAUW1kdhOK8']


    # title of the image
    caption = """Discover the endless possibilities of 
    data analysis with Coda Analytics. Our powerful analytics 
    platform empowers you to transform raw data into actionable 
    insights, enabling you to make informed decisions and drive your business forward. """
    for group_id in group_ids:
        pywhatkit.sendwhats_image(group_id, image_path, caption, 15, True, 6)