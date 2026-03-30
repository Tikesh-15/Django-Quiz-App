from django.contrib import admin
from .models import Exam, Question, Result

# 1. Questions ko Exam ke andar hi dikhane ke liye (Tujhe alag se Question tab mein nahi jana padega)
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3  # Shuruat mein 3 khali sawal dikhenge, aur bhi add kar sakte ho

# 2. Exam Model ko register karo
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    # Admin list mein kya-kya dikhega
    list_display = ('title', 'exam_code', 'duration_minutes', 'created_at')
    # Exam ke andar hi questions ka option
    inlines = [QuestionInline]

# 3. Result Model ko register karo taaki bacho ke marks dekh sako
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'percentage', 'completed_at')
    list_filter = ('exam', 'completed_at') # Filter karne ke liye side mein option aayega