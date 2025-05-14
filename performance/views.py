from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from .models import Employee, PerformanceReview, Goal, Feedback, SelfAssessment, Benefit, Enrollment, Review
from .serializers import (
    EmployeeSerializer, PerformanceReviewSerializer,
    GoalSerializer, FeedbackSerializer, SelfAssessmentSerializer, BenefitSerializer, EnrollmentSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class SelfAssessmentViewSet(viewsets.ModelViewSet):
    queryset = SelfAssessment.objects.all()
    serializer_class = SelfAssessmentSerializer


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.role == 'HR'

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.userprofile.role == 'MANAGER'

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsHR] 

class BenefitViewSet(viewsets.ModelViewSet):
    queryset = Benefit.objects.all()
    serializer_class = BenefitSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsHR()]
        return [permissions.IsAuthenticated()]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        if user_profile.role == 'EMPLOYEE':
            return Enrollment.objects.filter(employee=user_profile)
        return Enrollment.objects.all()

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.userprofile)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hr_dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role != 'HR':
        return Response({'detail': 'Not authorized.'}, status=403)

    total_employees = Employee.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    total_benefits = Benefit.objects.count()
    total_enrollments = Enrollment.objects.count()

    return Response({
        "total_employees": total_employees,
        "average_review_rating": round(avg_rating, 2),
        "total_benefits": total_benefits,
        "total_enrollments": total_enrollments
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_dashboard(request):
    user_profile = request.user.userprofile
    if user_profile.role != 'MANAGER':
        return Response({'detail': 'Not authorized.'}, status=403)

    feedback_count = Feedback.objects.filter(manager=request.user).count()
    reviews_given = Review.objects.filter(manager=request.user).count()

    return Response({
        "your_feedback_count": feedback_count,
        "reviews_given": reviews_given
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def self_assessment_view(request):
    if request.method == 'GET':
        employee = Employee.objects.get(user=request.user)
        assessments = SelfAssessment.objects.filter(employee=employee)
        serializer = SelfAssessmentSerializer(assessments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        employee = Employee.objects.get(user=request.user)
        data = request.data.copy()
        data['employee'] = employee.id 

        serializer = SelfAssessmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


