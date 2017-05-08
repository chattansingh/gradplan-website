"""gradplanproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views
#from plan.views import choose_a_major, view_major_job_salaries
from professorrating.views import rate_professor

from plan.views import choose_a_major, view_major_job_salaries


urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^home/', include('home.urls'), name='home'),
	url(r'^login/', auth_views.login, name='login'),
	url(r'^home/logout/', auth_views.logout, name='logout'),
	url(r'^accounts/', include('registration.backends.simple.urls'), name='accounts'),
	url(r'^profile/', include('accounts.urls'), name='profile'),
	url(r'^roadmap/', include('plan.urls'), name='road_map'),
	url(r'^choosemajor/', choose_a_major, name='choose_a_major'),
	url(r'^majorjobsalaires/', view_major_job_salaries, name='view_major_job_salaries'),
	url(r'^ratings/(?P<last_name>\w+)/(?P<first_name>\w+)/(?P<class_name>\w+)', rate_professor, name='rate_professor'),
	url(r'^$', RedirectView.as_view(url='/home/')),

]

