from django.conf.urls import url
from django.views.generic import TemplateView
from accounts.views import update_profile, suggest_major
from . import views

urlpatterns = [
    url(r'^suggest/', suggest_major, name='suggest_major'),
    url(r'^$', update_profile, name='user_profile'),
    # url(r'^submit/', views.update_profile, name='update_profile'),

]