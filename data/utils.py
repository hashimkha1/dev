def training_responses(request):
    value=request.path.split("/")
    path_values = [i for i in value if i.strip()]
    sub_title=path_values[-1]
    # # print(sub_title)
    # for activity in tasks:
    #     if activity.activity_name in ['Laptop','Schedules']:
    #         task_name=activity.activity_name
    #         task_question=activity.guiding_question
    #         print(task_name,task_question)
    return sub_title #,task_name,task_question