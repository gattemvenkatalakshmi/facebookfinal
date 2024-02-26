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

