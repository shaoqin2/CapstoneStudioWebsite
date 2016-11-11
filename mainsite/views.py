from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from mainsite.models import Student, Class, Parent


# Create your views here.
@login_required(login_url='/login/')
def home_page(request):
	return parse(request)

	

def parse(request):
	print (request.user)
	try:
		temp = Student.objects.get(userName=request.user)
	except Student.DoesNotExist:
		temp = None
				
	if temp is not None:
		return HttpResponseRedirect('/studentpage/homework')
	else:
		try:
			p = Parent.objects.get(userName=request.user)
		except Parent.DoesNotExist:
			p = None
		if p is not None:
			return HttpResponseRedirect('/parentpage/feedback')
		else:
			return HttpResponseRedirect('/teacherpage/')	

def student_homework(request):
	return HttpResponse("<h1>student_homework</h1>")
	
def parent_homework_status(request):
	return HttpResponse("<h1>parent_homework_status</h1>")

def parent_homework(request):
	return HttpResponse("<h1>parent_homework</h1>")

def parent_feedback(request):
	return HttpResponse("<h1>parent_feedback</h1>")
	
def teacher_page(request):
	return HttpResponse("<h1>teacher_page</h1>")
	
def login(request):
	return HttpResponse("login!")