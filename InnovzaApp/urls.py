from django.conf.urls import url
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^register$',views.register,name='register'),
    url(r'^verifyotp$', views.verifyotp, name="verifyotp"),
    url(r'^profile_photo$', views.profile_photo, name="profile_photo"),
    url(r'^post_info/$',views.post_info,name='post_info'),
    url(r'^post_update$',views.post_update,name='post_update'),
    path('post/<id>/',views.post,name='post-detail'),
    url(r'^blog/$', views.blog, name='post-list'),
    url(r'^userBlog$', views.userBlog, name='userBlog'),
    url(r'^userProject$', views.userProject, name='userProject'),
    url(r'^signin$',views.signin,name='signin'),
    url(r'^project_info/$',views.project_info,name='project_info'),
    url(r'^project_update$',views.project_update,name='project_update'),
    url(r'^projectinfo/$', views.projectinfo, name='project-list'),
    path('project/<id>/',views.project,name='project-detail'),
    url(r'^logoff$', views.logoff, name='logoff'),
    url(r'^userpage$',views.userpage,name='userpage'),
]