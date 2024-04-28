from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Survey(models.Model):
    """Represents a survey, which contains multiple questions."""
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        """Returns the title of the survey as its string representation."""
        return self.title

class Question(models.Model):
    """Represents a question within a survey. Questions can have dependencies on other questions."""
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('choice', 'Choice'),
        ('multiple', 'Multiple Choice')
    ]
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    is_required = models.BooleanField(default=False, help_text="Mark if this question must be answered.")
    dependent_on = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependencies')
    required_answers = models.ManyToManyField('Answer', blank=True, related_name='required_by_questions')

    def __str__(self):
        """Returns the question text as its string representation."""
        return self.text

class Answer(models.Model):
    """Represents an answer to a specific question, linked back to the Question model."""
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        """Returns the answer text as its string representation."""
        return self.text

class Response(models.Model):
    """Records a response to a survey question, associating answers with a user and a specific survey question."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """Returns a descriptive string of the response, including the user and related question."""
        return f'{self.user.username} response to {self.survey.title} for question {self.question.text}'

class UserResponse(models.Model):
    """Associates a user with their answer to a particular question."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Ответ")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")

    def __str__(self):
        """Returns a formatted string that includes user info and their selected answer to a question."""
        return f'{self.user.username} - {self.question.text} - {self.answer.text}'
