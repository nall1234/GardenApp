from django.db import models
import re
import bcrypt

class UserValidator(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 charaters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        email = postData['email']
        lower_email = email.lower()
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(lower_email):
            errors['email'] = 'Invalid Email address'
        email_check = User.objects.filter(email= postData['email'])
        if email_check:
            errors['email_check'] = 'User email already in use'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 charactors'
        if not postData['password'] == postData['confirm_password']:
            errors['confirm_password'] = 'Password must match'   
        return errors
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
                return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    image = models.ImageField ( null = True, blank = True, upload_to ="images/", default = 'images/blank.jpg')
    objects = UserValidator()
