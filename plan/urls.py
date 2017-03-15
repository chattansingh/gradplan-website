from django.conf.urls import url
from views import grad_road_map, view_major_job_salaries

urlpatterns = [
    url(r'^$', grad_road_map, name='grad_road_map'),


]