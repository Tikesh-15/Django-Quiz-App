from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Exam, Question, Result, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm

# 1. REGISTRATION: Teacher/Student account creation
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            is_teacher = True if role == 'teacher' else False
            UserProfile.objects.create(user=user, is_teacher=is_teacher)
            
            if is_teacher:
                user.is_staff = True
                user.save()
                
            messages.success(request, f"Account ban gaya! Ab Login karein.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 2. HOME VIEW: Exam code entry for students
def home(request):
    if request.method == "POST":
        code = request.POST.get('exam_code').upper()
        exam = Exam.objects.filter(exam_code=code).first()
        if exam:
            # Check if already attempted
            if request.user.is_authenticated:
                already_done = Result.objects.filter(user=request.user, exam=exam).exists()
                if already_done:
                    messages.warning(request, "Aap ye exam pehle hi de chuke hain!")
                    return redirect('home')
            return redirect('take_exam', exam_id=exam.id)
        else:
            messages.error(request, "Galat Code! Sahi code dalein.")
    return render(request, 'home.html')

# 3. TAKE EXAM: Main exam logic
@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    if request.method == "POST":
        score = 0
        total = questions.count()
        for q in questions:
            ans = request.POST.get(f'question_{q.id}')
            if ans and int(ans) == q.correct_option:
                score += 1
        
        percentage = (score / total) * 100 if total > 0 else 0
        res = Result.objects.create(
            user=request.user, exam=exam, score=score, 
            total_questions=total, percentage=round(percentage, 2)
        )
        return render(request, 'result.html', {'result': res})

    return render(request, 'take_exam.html', {'exam': exam, 'questions': questions})

# 4. MY RESULTS: Student exam history
@login_required
def my_results(request):
    results = Result.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'my_results.html', {'results': results})

# 5. TEACHER DASHBOARD: Exam management
@staff_member_required
def teacher_dashboard(request):
    exams = Exam.objects.filter(author=request.user).order_by('-created_at')
    if request.method == "POST":
        title = request.POST.get('title')
        duration = request.POST.get('duration')
        new_exam = Exam.objects.create(
            title=title, duration_minutes=duration, author=request.user
        )
        messages.success(request, f"Exam '{title}' ban gaya! Code: {new_exam.exam_code}")
        return redirect('teacher_dashboard')
    
    return render(request, 'teacher_dashboard.html', {'exams': exams})

# 6. ADD QUESTION: Add questions via frontend
@staff_member_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, author=request.user)
    if request.method == "POST":
        Question.objects.create(
            exam=exam,
            text=request.POST.get('text'),
            option1=request.POST.get('opt1'),
            option2=request.POST.get('opt2'),
            option3=request.POST.get('opt3'),
            option4=request.POST.get('opt4'),
            correct_option=request.POST.get('correct')
        )
        messages.success(request, "Sawal save ho gaya! Agla sawal dalein.")
        return redirect('add_question', exam_id=exam.id)
    
    return render(request, 'add_question.html', {'exam': exam})

# 7. LEADERBOARD: Student performance tracking
@staff_member_required
def view_exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, author=request.user)
    results = Result.objects.filter(exam=exam).order_by('-score')
    return render(request, 'exam_leaderboard.html', {'exam': exam, 'results': results})

@staff_member_required
def delete_exam(request, exam_id):
    # Sirf wahi teacher delete kar sake jisne banaya hai
    exam = get_object_or_404(Exam, id=exam_id, author=request.user)
    if request.method == "POST":
        exam.delete()
        messages.success(request, "Exam kamyabi se delete ho gaya!")
    return redirect('teacher_dashboard')

# 1. Saare sawal dekhne ke liye
@staff_member_required
def view_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, author=request.user)
    questions = exam.questions.all()
    return render(request, 'view_questions.html', {'exam': exam, 'questions': questions})

# 2. Sawal ko edit karne ke liye
@staff_member_required
def edit_question(request, q_id):
    question = get_object_or_404(Question, id=q_id, exam__author=request.user)
    if request.method == "POST":
        question.text = request.POST.get('text')
        question.option1 = request.POST.get('opt1')
        question.option2 = request.POST.get('opt2')
        question.option3 = request.POST.get('opt3')
        question.option4 = request.POST.get('opt4')
        question.correct_option = request.POST.get('correct')
        question.save()
        messages.success(request, "Sawal update ho gaya!")
        return redirect('view_questions', exam_id=question.exam.id)
    
    return render(request, 'edit_question.html', {'q': question})

# 3. Sirf sawal delete karne ke liye (Optional par zaroori)
@staff_member_required
def delete_question(request, q_id):
    question = get_object_or_404(Question, id=q_id, exam__author=request.user)
    exam_id = question.exam.id
    question.delete()
    messages.success(request, "Sawal delete kar diya gaya!")
    return redirect('view_questions', exam_id=exam_id)