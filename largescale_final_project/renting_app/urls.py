from django.conf.urls import include, url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login', views.user_login, name='login'),
  url(r'^logout/$', views.user_logout, name='logout'),
  url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
  url(r'^add-item/$', views.add, name='add-item'),
  url(r'^home/$', views.home, name='home'),
  url(r'^item/(?P<user_id>[0-9]+)/(?P<item_id>[0-9]+)', views.item, name='item'),
  url(r'^modify/$', views.modify, name='modify'),
  url(r'^search/$', views.search, name='search'),
]
