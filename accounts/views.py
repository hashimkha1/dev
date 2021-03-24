from django.shortcuts import render

# Create your views here.
#---------------Test----------------------
def join(request):
    return render(request, 'users/join.html', {'clients': clients})