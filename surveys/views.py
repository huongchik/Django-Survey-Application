from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Question, Answer, Response, UserResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction
from django.core.exceptions import ValidationError

def get_answers_for_question(request, question_id):
    """
    Provides a JSON response with answers for a given question.
    """
    answers = Answer.objects.filter(question_id=question_id)
    return JsonResponse(list(answers.values('id', 'text')), safe=False)

def register(request):
    """
    Handles user registration using Django's UserCreationForm.
    Redirects to survey list upon successful registration and login.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the newly registered user
            return redirect('surveys:survey_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    """
    Handles user login using Django's built-in AuthenticationForm.
    Redirects to survey list upon successful login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('surveys:survey_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def survey_list(request):
    """
    Displays a list of all available surveys.
    """
    surveys = Survey.objects.all()
    return render(request, 'surveys/survey_list.html', {'surveys': surveys})

@login_required
def survey_detail(request, pk):
    """
    Displays detailed view of a survey and handles survey responses submission.
    Ensures all required questions are answered, or provides error feedback.
    """
    survey = get_object_or_404(Survey, pk=pk)
    
    if request.method == 'POST':
        user = request.user
        mandatory_missing = []

        try:
            with transaction.atomic():
                for question in survey.questions.all():
                    response_collected = False
                    if question.question_type == 'text':
                        text_response = request.POST.get(str(question.id))
                        if text_response:
                            response = Response.objects.create(survey=survey, question=question, user=user)
                            answer = Answer.objects.create(question=question, text=text_response)
                            response.answers.add(answer)
                            UserResponse.objects.create(user=user, question=question, answer=answer)
                            response_collected = True
                    
                    elif question.question_type == 'choice':
                        answer_text = request.POST.get(str(question.id))
                        if answer_text:
                            answer, created = Answer.objects.get_or_create(question=question, text=answer_text)
                            response = Response.objects.create(survey=survey, question=question, user=user)
                            response.answers.add(answer)
                            UserResponse.objects.create(user=user, question=question, answer=answer)
                            response_collected = True
                    
                    elif question.question_type == 'multiple':
                        answer_texts = request.POST.getlist(str(question.id) + '[]')
                        if answer_texts:
                            response = Response.objects.create(survey=survey, question=question, user=user)
                            for text in answer_texts:
                                answer, created = Answer.objects.get_or_create(question=question, text=text)
                                response.answers.add(answer)
                                UserResponse.objects.create(user=user, question=question, answer=answer)
                            response_collected = True
                    
                    if question.is_required and not response_collected:
                        mandatory_missing.append(question.text)

                if mandatory_missing:
                    raise ValidationError("Please answer all required questions: " + ", ".join(mandatory_missing))

        except ValidationError as e:
            return render(request, 'surveys/survey_detail.html', {'survey': survey, 'error': str(e)})

        return redirect('surveys:survey_list')

    return render(request, 'surveys/survey_detail.html', {'survey': survey})
