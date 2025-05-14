from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, PerformanceReviewViewSet,
    GoalViewSet, FeedbackViewSet, SelfAssessmentViewSet, BenefitViewSet, EnrollmentViewSet, hr_dashboard, manager_dashboard, self_assessment_view
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'reviews', PerformanceReviewViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'self-assessments', SelfAssessmentViewSet)
router.register(r'benefits', BenefitViewSet)
router.register(r'enrollments', EnrollmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/hr/', hr_dashboard),
    path('dashboard/manager/', manager_dashboard),
    path('self-assessment/', self_assessment_view),

]
