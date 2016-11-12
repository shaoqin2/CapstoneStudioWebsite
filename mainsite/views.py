from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as LOGIN, logout as LOGOUT
from django.contrib.auth.decorators import login_required
from mainsite.models import Student, Class, Parent
from mainsite import forms


# Create your views here.
@login_required(login_url='/login/')
def home_page(request):
	return parse(request)

	
@login_required(login_url='/login/')
def parse(request):
	print (request.user)
	try:
		temp = Student.objects.get(username=request.user)
	except Student.DoesNotExist:
		temp = None
				
	if temp is not None:
		return HttpResponseRedirect('/studentpage/homework')
	else:
		try:
			p = Parent.objects.get(username=request.user)
		except Parent.DoesNotExist:
			p = None
		if p is not None:
			return HttpResponseRedirect('/parentpage/feedback')
		else:
			return HttpResponseRedirect('/teacherpage/')	
@login_required(login_url='/login/')
def student_homework(request):
	student = Student.objects.get(username=request.user)
	dict = student.get_homework()
	return render(request,'StudentPage.html',dict)
	
	
@login_required(login_url='/login/')	
def parent_homework_status(request):
	return HttpResponse("<h1>parent_homework_status</h1>")
	
	
@login_required(login_url='/login/')
def parent_homework(request):
	return HttpResponse("<h1>parent_homework</h1>")
	
	
	
@login_required(login_url='/login/')
def parent_feedback(request):
	return HttpResponse("<h1>parent_feedback</h1>")
	

@login_required(login_url='/login/')	
def teacher_page(request):
	return HttpResponse("<h1>teacher_page</h1>")
	
def login(request):
	form = forms.loginForm()
	error = ""
	if request.method=='POST':
		form = forms.loginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
			if user is not None:
				LOGIN(request,user)
				return HttpResponseRedirect('/parse/')
			else:
				error = "Invalid Password or Username"
		else:
			error = "Please input valid credentials"
	return render(request,"defaultlogin.html",{"form":form,"error":error})
	

	
def logout(request):
	LOGOUT(request)
	return HttpResponseRedirect('/')
	
	
	
	
	
	
	