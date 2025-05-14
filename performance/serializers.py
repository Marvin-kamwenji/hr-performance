from rest_framework import serializers
from .models import Employee, PerformanceReview, Goal, Feedback, SelfAssessment, Benefit, Enrollment

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SelfAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfAssessment
        fields = '__all__'


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
