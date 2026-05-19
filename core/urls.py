from django.urls import path

from .views import docs_page, health_check, home_view, show_prompts

urlpatterns = [
    path('', home_view, name='home'),
    path('prompts/', show_prompts, name='prompts'),
    path('docs/', docs_page, name='docs'),
    path('health/', health_check, name='health_check'),
]

