from django.forms import ModelForm
from .models import User, Post
from django.contrib.auth.hashers import make_password


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    def save(self, commit=True):         
        instance = super(UserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            instance.password = make_password(password)
        if commit:
            instance.save()
        return instance 


class  UserFormToExcludeFields(UserForm):
    class Meta(UserForm.Meta):
        exclude = ['phone_number', 'first_name',
                   'surname', 'date_of_birth', 'gender']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['media_file', 'info_about_photo']