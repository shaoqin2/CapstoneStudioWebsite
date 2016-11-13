from django.contrib import admin
from mainsite.models import Student, Teacher, Class, Homework, Feedback, Parent
from datetime import date
from django.utils.translation import ugettext_lazy as _
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
	list_display = ('name_chinese',)
admin.site.register(Student, StudentAdmin)


class ClassAdmin(admin.ModelAdmin):
	list_display = ('name_chinese', 'name', 'class_has_end')
	filter_horizontal = ('enrolled_student','teacher')
admin.site.register(Class, ClassAdmin)


class HomeworkFilter(admin.SimpleListFilter):
	title = _('due_date')
	parameter_name = 'due_date'
	
	def lookups(self, request, HomeworkAdmin):
		return (
			('og',_('ongoingHomework')),
			('ad',_('pastHomework'))
		)
	def queryset(self, request, queryset):
		if self.value()=='og':
			for i in queryset:
				print (i.dueDate)
			return queryset.filter(due_date__gte=date.today())
		if self.value()=='ad':
			return queryset.filter(due_date__lt=date.today())

class HomeworkAdmin(admin.ModelAdmin):
	list_display = ('name_chinese','belong_to_class','assigned_by','due_date','report','submission')
	list_filter = (HomeworkFilter,)
	filter_horizontal = ('completed_student',)
admin.site.register(Homework,HomeworkAdmin)

class FeedBackAdmin(admin.ModelAdmin):
	list_display = ('name','for_student')
admin.site.register(Feedback,FeedBackAdmin)


class ParentAdmin(admin.ModelAdmin):
	list_display = ('name_chinese','student')
admin.site.register(Parent,ParentAdmin)

admin.site.register(Teacher)