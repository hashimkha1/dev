import traceback
from django.http import Http404

# from getdata.models import Logs


class MailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        status_code = 500 if isinstance(exception, Http404) else 500
        if status_code == 500:
            error = traceback.format_exc()
            error_line = error.splitlines()
            flag = 0
            error_line_no = None
            reason_error = None
            for line in error_line:
                if request.path.split("/")[1] in line or flag == 1:
                    if flag == 1:
                        reason_error = line
                        break
                    error_line_no = line
                    flag = 1
            # Logs.objects.create(api=request.path, location_in_code=error_line_no, reason_code_crash=reason_error,
            #                     user_id=request.user.id, exception=exception.args)

        return          # no return anything