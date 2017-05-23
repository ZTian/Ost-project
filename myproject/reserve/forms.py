from django import forms
from .models import Resource, Reservation, Tag
from django.contrib.auth import authenticate, get_user_model, login, logout
import datetime

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user_qs = User.objects.filter(username=username)
        if user_qs.count() == 0:
            raise forms.ValidationError("This user does not exist")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Incorrect password")
        if not user.is_active:
            raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Password does not match")
        return password

class ResourceCreateForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),required=False)
    class Meta:
        model = Resource
        fields = [
            'title',
            'start_time',
            'end_time',
            'tag',
            'resource_logo',
            'resource_description',
        ]

    def clean(self, *args, **kwargs):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if end_time <= start_time:
            raise forms.ValidationError("Time ends before start!")
        return super(ResourceCreateForm, self).clean(*args, **kwargs)

class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'resource',
            'date_time',
            'start_time',
            'end_time',
        ]

    def clean(self, *args, **kwargs):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        date_time = self.cleaned_data.get("date_time")
        target_resource = self.cleaned_data.get("resource")
        resource_list = Resource.objects.filter(pk = target_resource.pk)
        if end_time <= start_time:
            raise forms.ValidationError("Time ends before start!")
        if date_time < datetime.date.today():
            raise forms.ValidationError("Date has already passed!")
        if date_time == datetime.date.today() and end_time < datetime.datetime.today().time():
            raise forms.ValidationError("Reservation has already passed!")
        for resource in resource_list:
            if not (end_time <= resource.end_time and start_time >= resource.start_time):
                raise forms.ValidationError("Not available at that time!")
        reservation_list = Reservation.objects.filter(resource=target_resource)
        for reservation in reservation_list:
            if date_time == reservation.date_time:
                if start_time >= reservation.start_time and start_time < reservation.end_time:
                    raise forms.ValidationError("Reserved by others!")
                if end_time > reservation.start_time and end_time <= reservation.end_time:
                    raise forms.ValidationError("Reserved by others!")
                if start_time <= reservation.start_time and end_time >= reservation.end_time:
                    raise forms.ValidationError("Reserved by others!")
        return super(ReservationCreateForm, self).clean(*args, **kwargs)

class ReserveResourceForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'date_time',
            'start_time',
            'end_time',
        ]

    def clean(self, *args, **kwargs):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        date_time = self.cleaned_data.get("date_time")
        if end_time <= start_time:
            raise forms.ValidationError("Time ends before start!")
        if date_time < datetime.date.today():
            raise forms.ValidationError("Date has already passed!")
        if date_time == datetime.date.today() and end_time < datetime.datetime.today().time():
            raise forms.ValidationError("Reservation has already passed!")
        return super(ReserveResourceForm, self).clean(*args, **kwargs)

class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'title',
        ]