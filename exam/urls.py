from django.urls import path
from . import views

urlpatterns = [
    # Students ke liye
    path('', views.home, name='home'),
    path('take-exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('register/', views.register, name='register'),
    # Tere liye (Teacher/Creator) - Frontend se Question/Time add karne ke liye
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add-question/<int:exam_id>/', views.add_question, name='add_question'),
    path('my-results/', views.my_results, name='my_results'),
    path('exam-results/<int:exam_id>/', views.view_exam_results, name='view_exam_results'),
    path('delete-exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('exam/<int:exam_id>/questions/', views.view_questions, name='view_questions'),
path('question/edit/<int:q_id>/', views.edit_question, name='edit_question'),
path('question/delete/<int:q_id>/', views.delete_question, name='delete_question'),
]