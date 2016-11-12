"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from mainsite import views
urlpatterns = [
	url(r'^$',views.home_page,name='HomePage'),
	url(r'^parse/$',views.parse,name='Parse'),
	url(r'^login/',views.login,name='Login'),
	url(r'^studentpage/homework/',views.student_homework,name="StudentHomework"),
	url(r'^teacherpage/',views.teacher_page,name="TeacherPage"),
	url(r'^parentpage/homeworkstatus',views.parent_homework_status,name = "ParentHomeworkStatus"),
	url(r'^parentpage/homework',views.parent_homework,name = "ParentHomework"),
	url(r'^parentpage/feedback',views.parent_feedback,name="ParentFeedback"),
	url(r'^logout/',views.logout,name='Logout'),
]
