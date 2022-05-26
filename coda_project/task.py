from celery import shared_task

from management.models import Task, TaskHistory


@shared_task(name="task_history")
def dump_data():
    try:
        bulk_object = []
        get_data = Task.objects.all()
        for data in get_data:
            bulk_object.append(
                TaskHistory(
                    group=data.group,
                    category=data.category,
                    employee=data.employee,
                    activity_name=data.activity_name,
                    description=data.description,
                    slug=data.slug,
                    duration=data.duration,
                    point=data.point,
                    mxpoint=data.mxpoint,
                    mxearning=data.mxearning,
                    submission=data.submission,
                    is_active=data.is_active,
                    featured=data.featured,
                )
            )
        TaskHistory.objects.bulk_create(bulk_object)
        get_data.update(point=0)
        return True
    except Exception:
        return False
