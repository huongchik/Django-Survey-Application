from django.urls import path
from . import views

app_name = 'surveys'
urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('<int:pk>/', views.survey_detail, name='survey_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('questions/<int:question_id>/answers/', views.get_answers_for_question, name='question_answers'),
]
