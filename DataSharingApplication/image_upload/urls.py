from django.conf.urls import url
from . import views


app_name='image_upload'

urlpatterns=[
    url(r'^(?i)$',views.login,name='login'),
    url(r'^logout(?i)/$',views.logout,name='logout'),
    url(r'^login(?i)/$',views.login,name='login'),
    url(r'^index(?i)/$',views.index,name='index'),
    url(r'^register(?i)/$',views.rgister,name='register'),
    url(r'^send_to_user(?i)/$',views.send_to_user.as_view(),name='send_to_user'),
    url(r'^delete_from_aws(?i)/$',views.delete_from_aws.as_view(),name='delete_from_aws'),
    url(r'^download(?i)/$',views.download,name='download'),


]
