from django.conf.urls import url
from views import grad_road_map, view_major_job_salaries, modify_gradplan

urlpatterns = [
    url(r'^$', grad_road_map, name='grad_road_map'),
    url(r'^modifyplan', modify_gradplan, name='modify_grad_plan')

]