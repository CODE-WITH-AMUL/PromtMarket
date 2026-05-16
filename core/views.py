from django.shortcuts import render

# Create your views here.


def Home(request):
    template_name = 'home.html'
    return render(request, template_name)