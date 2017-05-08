from django.conf.urls import url
from views import grad_road_map, view_major_job_salaries, modify_gradplan, choose_semester, current_semester,common_classes

urlpatterns = [
    url(r'^$', grad_road_map, name='grad_road_map'),
    url(r'^modifyplan', modify_gradplan, name='modify_grad_plan'),
    url(r'^choosesemester', choose_semester, name='choose_semester'),
    url(r'^currentsemester', current_semester, name='current_semester'),
    url(r'^commonclasses', common_classes, name='common_classes'),

]