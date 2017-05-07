from django.conf.urls import url
from django.views.generic import TemplateView
from accounts.views import update_profile, suggest_major, edit_classes
from . import views

urlpatterns = [
    url(r'^suggest/', suggest_major, name='suggest_major'),
    url(r'^removeclasses/', edit_classes, name='edit_classes'),
    url(r'^$', update_profile, name='user_profile'),

    # url(r'^submit/', views.update_profile, name='update_profile'),

]
