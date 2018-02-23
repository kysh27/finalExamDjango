from django.conf.urls import url
from addbook import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'home/$', views.home, name='home'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'add/$', views.add_new, name='addnew'),
    url(r'import/$', views.csv_import, name='importcsv'),
    url(r'addbook/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'addbook/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
]