from django.contrib import admin
from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from django.forms.models import BaseInlineFormSet
from .models import Survey, Question, Answer, Response
from django.core.exceptions import ValidationError

class QuestionForm(forms.ModelForm):
    """Form for creating and updating Question instances. Includes custom validation for dependent questions."""
    
    class Meta:
        model = Question
        fields = '__all__'

    def clean_required_answers(self):
        """Custom clean method to ensure required answers are valid for questions with dependencies."""
        required_answers = self.cleaned_data.get('required_answers')
        dependent_on = self.cleaned_data.get('dependent_on')

        if dependent_on:
            valid_answers_ids = Answer.objects.filter(question=dependent_on).values_list('id', flat=True)
            invalid_answers = [answer.id for answer in required_answers if answer.id not in valid_answers_ids]

            if invalid_answers:
                raise ValidationError(f"Select a valid choice. {invalid_answers} are not valid choices.")

        return required_answers


class AnswerInlineFormSet(BaseInlineFormSet):
    """Custom formset for managing Answer instances inline in the Question admin."""
    
    def __init__(self, *args, **kwargs):
        super(AnswerInlineFormSet, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.queryset = Answer.objects.filter(question=self.instance)

class AnswerInline(admin.TabularInline):
    """Inline admin to manage answers directly from the question page."""
    model = Answer
    formset = AnswerInlineFormSet
    extra = 3

    def get_queryset(self, request):
        """Custom queryset filtering based on the current question being edited."""
        qs = super().get_queryset(request)
        if 'object_id' in request.resolver_match.kwargs:
            question_id = request.resolver_match.kwargs['object_id']
            qs = qs.filter(question__id=question_id)
        return qs

class QuestionInline(admin.TabularInline):
    """Inline admin for adding questions directly on the survey page."""
    model = Question
    extra = 1
    show_change_link = True

class SurveyAdmin(admin.ModelAdmin):
    """Admin view for managing surveys."""
    list_display = ['title', 'start_date', 'end_date']
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    """Admin view for managing questions."""
    class Media:
        js = ('js/admin_custom.js',)  # Path to custom JavaScript file for the admin page.

    form = QuestionForm
    list_display = ['text', 'survey', 'question_type']
    inlines = [AnswerInline]

class AnswerAdmin(admin.ModelAdmin):
    """Admin view for managing answers."""
    list_display = ['text', 'question']

class ResponseAdminForm(ModelForm):
    """Form for creating and updating Response instances, restricting answer choices based on the question."""
    
    answers = ModelMultipleChoiceField(queryset=Answer.objects.none())

    class Meta:
        model = Response
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ResponseAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.question_id:
            self.fields['answers'].queryset = Answer.objects.filter(question=instance.question)
        else:
            self.fields['answers'].queryset = Answer.objects.none()

class ResponseAdmin(admin.ModelAdmin):
    """Admin view for managing responses."""
    form = ResponseAdminForm
    list_display = ['survey', 'question', 'user']
    list_filter = ['survey', 'user']

    def get_queryset(self, request):
        """Custom queryset to limit visibility based on user permissions."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

# Registration of admin panels
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Response, ResponseAdmin)
