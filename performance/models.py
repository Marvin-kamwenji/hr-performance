from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_joined = models.DateField()

    def __str__(self):
        return self.name

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Employee, related_name='reviews_given', on_delete=models.CASCADE)
    review_date = models.DateField()
    overall_score = models.DecimalField(max_digits=4, decimal_places=2)
    comments = models.TextField()

    def __str__(self):
        return f'Review for {self.employee.name} by {self.reviewer.name}'

class Goal(models.Model):
    employee = models.ForeignKey(Employee, related_name='goals', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Goal: {self.title} for {self.employee.name}'

class Feedback(models.Model):
    from_employee = models.ForeignKey(Employee, related_name='feedback_given', on_delete=models.CASCADE)
    to_employee = models.ForeignKey(Employee, related_name='feedback_received', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.from_employee.name} to {self.to_employee.name}'

class SelfAssessment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review = models.ForeignKey(PerformanceReview, on_delete=models.CASCADE)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Self-assessment by {self.employee.name}'
    

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Benefit(models.Model):
    CATEGORY_CHOICES = (
        ('HEALTH', 'Health Insurance'),
        ('RETIREMENT', 'Retirement Plan'),
        ('WELLNESS', 'Wellness Program'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    available_to = models.ManyToManyField(UserProfile, related_name="available_benefits")

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} enrolled in {self.benefit.name}"

class Review(models.Model):
    employee = models.ForeignKey(UserProfile, related_name='reviews', on_delete=models.CASCADE)
    manager = models.ForeignKey(UserProfile, related_name='reviews_given', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review_date = models.DateField(auto_now_add=True)
    comments = models.TextField()

    def __str__(self):
        return f"Review for {self.employee.user.username} by {self.manager.user.username}"

    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)