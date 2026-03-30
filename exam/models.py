from django.db import models
from django.contrib.auth.models import User
import uuid

# 1. Exam Model: Jisme Exam ki details aur Unique Code hoga
class Exam(models.Model):
    # 'author' field se pata chalega ki ye exam kisne banaya hai (Privacy Fix)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_exams', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Unique 6-digit code jo user ko share karenge
    exam_code = models.CharField(max_length=8, unique=True, editable=False)
    duration_minutes = models.PositiveIntegerField(default=30, help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.exam_code:
            # Random 6 digit unique code generate hoga
            self.exam_code = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.exam_code})"

# 2. Question Model: MCQ questions ke liye
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    # 1 se 4 tak correct option choose karenge
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return f"Q: {self.text[:50]}"

# 3. Result Model: Student ka score save karne ke liye
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title} ({self.score})"

# 4. User Profile: Role check karne ke liye (Teacher vs Student)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Teacher' if self.is_teacher else 'Student'}"