from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'projectmanagement/home.html', {'title': 'home'})

def construction(request):
    return render(request, 'projectmanagement/construction.html', {'title': 'construction'})