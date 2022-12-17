import pywhatkit as pwk
from time import sleep


def send_msg_for_group(group_id, group_msg, gh, gm, gd):
    sleep(10)
    pwk.sendwhatmsg_to_group(group_id, group_msg, gh, gm, gd)


def send_img(msg_contact, img_path, img_title, send_delay):
    pwk.sendwhats_image(msg_contact, img_path, img_title, send_delay)


def send_msg_for_many_groups():
    grp_id_list = []
    content_of_msg = "Type your message here"
    msg_hour = 0
    msg_min = 0
    send_delay = 10
    img_title = "Type your image title here"
    img_path = "Type your image path here"

    for i in range(grp_id_list):
        if img_path is not None:
            send_img(grp_id_list[i], img_path, img_title, send_delay)
        else:
            send_msg_for_group(
                grp_id_list[i], content_of_msg, msg_hour, msg_min, send_delay
            )