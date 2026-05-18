from .views import *
from django.urls import path

urlpatterns = [
    path('', Home, name='home'),
    path('prompts/', show_prompts, name='prompts'),
    path('docs/', docs_page, name='docs'),
]

