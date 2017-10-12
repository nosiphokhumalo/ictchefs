from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from adminapp import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^login-form/$', views.LoginPageView.as_view()),
    url(r'^add/$', login_required(login_url='/login/')(views.AddPageView.as_view())),
    url(r'^viewStudents/', views.viewStudent, name = 'viewStudent'),
    url(r'^viewGraduates/', views.viewGraduate, name = 'viewGraduate'),
    url(r'^viewDropouts/', views.viewDropout, name = 'viewDropout'),
    url(r'^statistics/$', login_required(login_url='/login/')(views.StatisticsPageView.as_view())),
    url(r'^students/$', login_required(login_url='/login/')(views.StudentList.as_view())),
    url(r'^filter/', views.filter, name='filter'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
