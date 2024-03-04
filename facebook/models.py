from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from dateutil.relativedelta import relativedelta


# Create your models here.
class custom_validators:
    #  def  no_special_characters_field(text):
    def validate_is_older_than_thirteen(value):
        if value is not None:
            cutoff_date = timezone.now().date() - relativedelta(years=13)
            if value > cutoff_date:
                raise ValidationError('Age should be greater than 13 years')


    def validate_no_special_characters(value):
        if not value.isalpha():
            raise ValidationError(
                _('name should not contain special characters'),
                params={'value': value},
            )
   
        


class User(models.Model):
    gender_choices = [("Female", 'female'),
                      ("Male", 'male'), ("Custom", 'custom')]
    first_name = models.CharField(max_length=30, validators=[
                                  custom_validators.validate_no_special_characters,MaxLengthValidator(30)])
    surname = models.CharField(max_length=40, validators=[
        custom_validators.validate_no_special_characters])
    phone_number = PhoneNumberField(blank=True,unique = True)
    email_address = models.EmailField(max_length=30,unique = True)
    password = models.CharField(max_length=300, validators=[
        MinLengthValidator(8),
        MaxLengthValidator(300),
        validate_password
    ])
    
    date_of_birth = models.DateField(
        validators=[custom_validators.validate_is_older_than_thirteen])
    gender = models.CharField(max_length=20, choices=gender_choices)
    profile_picture = models.ImageField(null=True, blank= True,upload_to='images/' , default='/home/venkatalakshmi/FacebookFinal/facebook/static/images/user.png')
    cover_picture = models.ImageField(null=True, blank= True,upload_to='images/' , default='/home/venkatalakshmi/FacebookFinal/facebook/static/images/white.jpg')

class Friendship(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_friendships')

class Post(models.Model):
     User_id = models.ForeignKey(User, on_delete = models.CASCADE,related_name ='Stories')
     Created_Time = models.DateTimeField(auto_now_add=True)
     media_file = models.FileField(upload_to='images/')
     likes = models.IntegerField(null=True,blank=True,default=0)
     info_about_photo= models.TextField(null=True,blank=True)
     comments = models.IntegerField(null=True, blank= True, default=0 )

class FriendRequest(models.Model):
    from_user=models.ForeignKey(User,related_name="from_user",on_delete= models.CASCADE )
    to_user = models.ForeignKey(User, related_name="to_user",on_delete = models.CASCADE)
    status = models.TextField(default='pending')


class Like(models.Model):
     post_id = models.ForeignKey(Post,on_delete = models.CASCADE, related_name ='PostLikes')     
     from_user_id =models.ForeignKey(User,on_delete=models.CASCADE, related_name ='PostLikes')


class Comment(models.Model):
     post_id = models.ForeignKey(Post,on_delete=models.CASCADE,related_name= 'PostComments')
     commented_time = models.DateTimeField(auto_now_add= True)
     from_user_id = models.ForeignKey(User, on_delete = models.CASCADE)
     Comment_text = models.CharField(max_length=3000, null = True)