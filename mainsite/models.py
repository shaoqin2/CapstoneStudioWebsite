from django.db import models
from django.contrib.auth.models import User
from datetime import date



class Student(models.Model):
	name_chinese = models.CharField('中文名',max_length=80)
	username = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to = {'is_staff':False})
	join_date = models.DateField('加入时间',auto_now_add=True)
	email = models.EmailField(blank=True)
	phone_number = models.CharField(max_length = 18, blank=True)
	toefl_score = models.CharField(max_length= 4, blank=True)
	sat_score = models.CharField(max_length = 5,blank=True)
	act_score = models.CharField(max_length = 3,blank=True)
	
	def __str__(self):
		return str(self.name_chinese)
	
	
	def get_homework(self):
		'''get all homeworks of classes related to this student'''
		dict = {}
		dict['notification'] = False
		dict['content'] = {}
		for my_class in self.related_class.all():
			homework_list = []
			for class_homework in my_class.related_homework.filter(due_date__gte=date.today()):
				if class_homework.due_date == date.today():
					dict['notification'] = True
				homework = {}
				homework['name_chinese'] = class_homework.name_chinese
				homework['assigned_by'] = class_homework.assigned_by
				homework['homework_content'] = class_homework.homework_content
				homework['assign_date'] = class_homework.assign_date
				homework['due_date'] = class_homework.due_date
				homework['submission'] = class_homework.submission
				homework_list.append(homework)
			dict['content'][my_class.name_chinese] = homework_list
		return dict
	
	
	def get_feedback(self):
		'''get all feedback to this student'''
		feedback_list =[]
		for my_feedback in self.related_feedback.order_by('-date')[:10]:
			feedback = {}
			feedback['name'] = my_feedback.name
			feedback['date'] = my_feedback.date
			feedback['feedback_content'] = my_feedback.feedback_content
			feedback['for_class'] = my_feedback.for_class
			feedback_list.append(feedback)
		feedback_dict = {}
		feedback_dict['content'] = feedback_list
		return feedback_dict
		
	def get_class(self):
		'''get all class this student enrolled'''
		pass
	
	def get_homework_status(self):
		'''get the homework status of this student'''
		ans = {}
		dict = {}
		for my_class in self.related_class.all():
			homeworkstatus_list = []
			count = 2
			for class_homework in my_class.related_homework.filter(due_date__lt=date.today()):
				if not class_homework.report:
					continue
				if count < 0:
					break
				homework = {}
				homework['name_chinese'] = class_homework.name_chinese
				homework['assigned_by'] = class_homework.assigned_by
				homework['homework_content'] = class_homework.homework_content
				homework['assign_date'] = class_homework.assign_date
				homework['due_date'] = class_homework.due_date
				homework['submission'] = class_homework.submission
				if self.completed_homework.filter(name_chinese=class_homework.name_chinese).exists():
					homework['status'] = '已完成'
				else:
					homework['status'] = '未完成'
				count -= 1
				homeworkstatus_list.append(homework)
			dict[my_class.name_chinese] = homeworkstatus_list
		ans['content'] = dict
		return ans
					
		
class Teacher(models.Model):
	name_chinese = models.CharField("中文名", max_length = 100)
	username = models.OneToOneField(User,on_delete=models.CASCADE, limit_choices_to = {'is_staff':True})
	def __str__(self):
		return str(self.name_chinese)
		
class Class(models.Model):
	name_chinese = models.CharField("中文名", max_length=300)
	name = models.CharField('课程编号', max_length=300)
	start_date = models.DateField('开课日期', auto_now_add=True)
	teacher = models.ManyToManyField(Teacher)
	enrolled_student = models.ManyToManyField(Student,related_name="related_class",verbose_name='学生')
	class_has_end = models.BooleanField('课程结束', default = False)
	def __str__(self):
		return self.name_chinese
		
		
		
class Homework(models.Model):
	name_chinese = models.CharField('作业名',max_length=100)
	assigned_by = models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name = "related_homework",verbose_name='布置老师')
	belong_to_class = models.ForeignKey(Class,on_delete=models.CASCADE,related_name = "related_homework",verbose_name='所属课程')
	report = models.BooleanField("反馈给家长？", default = False)
	homework_content = models.TextField('作业内容',max_length=5000)
	assign_date = models.DateField('布置日期')
	due_date = models.DateField('截止日期')
	
	
	submissionChoice = (("Submit by Email","Submit by Email"),("Submit in Person","Submit in Person"),("Submit by Wechat","Submit by Wechat"),("Submit in Class","Submit in Class"),("No need to Submit","No need to Submit"))
	submission = models.CharField('提交方式',max_length=20,choices=submissionChoice,default="Submit by Wechat")
	
	
	completed_student = models.ManyToManyField(Student,blank = True,verbose_name='已完成的学生',related_name='completed_homework')
	
	def __str__(self):
		return str(self.name_chinese)
		
class Parent(models.Model):
	name_chinese = models.CharField('中文名', max_length=50)
	username = models.OneToOneField(User,primary_key=True, limit_choices_to = {'is_staff':False})
	student = models.OneToOneField(Student,verbose_name='对应学生')
	phone_number = models.CharField(max_length=15, blank=True)
	email = models.EmailField(blank=True)
	def __str__(self):
		return str(self.name_chinese)
	# def getHomeworkStatus(self):
		# Stu = self.student
		# dict = {}
		# every cla is one class the kid has enrolled in
		# for cla in Stu.enrolledclass.all():
			# a = []
			# every hw is one class homework
			# for hw in cla.classHomework.order_by("-dueDate")[:4]:
				# print (hw)
				# homework hasn't due, teacher choose to report and is within 4 items
				# if hw.dueDate<date.today() and hw.report:
					# temp = {}
					# temp["name"] = hw.name
					# temp["dueDate"] = hw.dueDate
					# temp["assignedby"] = hw.assignedBy.name_chinese
					# if Stu in hw.completed.all():
						# temp["status"] = "Finished"
					# else:
						# temp["status"] = "unfinished"
					# temp["content"] = hw.homeworkContent
					# a.append(temp)
			# dict[cla.name_chinese] = a
		# return dict

		
class Feedback(models.Model):
	name = models.CharField('反馈名称',max_length = 200)
	for_class = models.ForeignKey(Class)
	for_student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name = "related_feedback")
	
	feedback_content = models.TextField(max_length = 5000)
	from_teacher = models.CharField(max_length=100,blank=True)
	date = models.DateField()	
	
	def __str__(self):
		return str(self.name)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
