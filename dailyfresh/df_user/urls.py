from django.conf.urls import url
import views

urlpatterns = [
    url('^login/$',views.login),
    url('^login_handle/$',views.login_handle),
    url('^logout/$',views.logout),
    url('^register/$',views.register),
    url('^register_exist/$',views.register_exist),
    url('^register_handle/$',views.register_handle),
]