# TASchedulerApp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import MyCourse, MyUser
from .models import LabSection, MyCourse, MyUser

class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Administrator', 'Administrator'),
        ('Instructor', 'Instructor'),
        ('TA', 'TA'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['name', 'email', 'role', 'password1', 'password2']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if MyUser.objects.filter(name=name).exists():
            raise ValidationError("A user with that username already exists.")
        return name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # Create the user but don't save yet
        user = super().save(commit=False)
        user.username = self.cleaned_data['name']

        # Hash the password before saving
        user.set_password(self.cleaned_data['password1'])

        # If commit is True, save the user instance
        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'role']
        
class CourseForm(forms.ModelForm):
    instructor = forms.ModelChoiceField(
        queryset=MyUser.objects.filter(role='Instructor'),
        required=True,
        label="Instructor"
    )

    class Meta:
        model = MyCourse
        fields = ['name', 'instructor', 'room', 'time']

class CourseAssignmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=MyCourse.objects.all(),
        label="Select Course"
    )
    instructor = forms.ModelChoiceField(
        queryset=MyUser.objects.filter(role='Instructor'),
        label="Select Instructor",
        required=False
    )
    tas = forms.ModelMultipleChoiceField(
        queryset=MyUser.objects.filter(role='TA'),
        label="Select TAs",
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class LabSectionForm(forms.ModelForm):
    class Meta:
        model = LabSection
        fields = ['name', 'section', 'course', 'instructor', 'ta']
        # 'course', 'instructor', and 'ta' fields can leverage
        # limit_choices_to from the model, or you can filter them here too.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, refine queryset if needed:
        self.fields['instructor'].queryset = MyUser.objects.filter(role='Instructor')
        self.fields['ta'].queryset = MyUser.objects.filter(role='TA')