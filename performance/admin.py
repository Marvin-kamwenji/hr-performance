from django.contrib import admin

from .models import Employee, PerformanceReview, Goal, Feedback, SelfAssessment

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'department', 'date_joined')
    search_fields = ('name', 'email', 'position', 'department')

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'overall_score')
    search_fields = ('employee__name', 'reviewer__name')
    list_filter = ('review_date',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('from_employee', 'to_employee', 'created_at')
    search_fields = ('from_employee__name', 'to_employee__name')

@admin.register(SelfAssessment)
class SelfAssessmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review', 'submitted_at')
