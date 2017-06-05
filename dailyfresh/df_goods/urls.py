from django.conf.urls import url
import views

urlpatterns = [
    url('^$',views.index),
    url(r'list(\d+)_(\d+)_(\d+)',views.list),
    url('^(\d+)',views.detail),
    url('^search/$',views.MySearchView())
]