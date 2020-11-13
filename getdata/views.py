from django.shortcuts import render

# views on ratings data.
def getrating(request):
    return render(request, 'getdata/getrating.html', {'title': 'getrating'})

def index(request):
    return render(request, 'getdata/index.html', {'title': 'index'})