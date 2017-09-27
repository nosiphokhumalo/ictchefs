from django.conf.urls import url
from adminapp import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^menu/$', views.MenuPageView.as_view()),
    url(r'^add/$', views.AddPageView.as_view()),
    url(r'^statistics/$', views.StatisticsPageView.as_view()),
    url(r'^students/', views.StudentList.as_view(), name='students'),
    url(r'^filter/', views.filter, name='filter'),
]
