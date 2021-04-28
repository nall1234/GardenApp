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


#-----MARKET ITEMS-----
class ItemManager(models.Manager):
    def item_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['item_title']) <= 1:
            errors['item_title'] = "Title name is required" 
        if len(reqPOST['item_description']) == 0:
            errors['item_description'] = "Description is required"
        if len(reqPOST['item_description']) < 5:
            errors['item_description'] = "Description should be at least 5 characters"
            errors['price'] = "Price is required"
        # if len(reqPOST['item_photo']) == 0:
        #     errors['item_photo'] = "Photo is required"
        return errors


class Item(models.Model):
    item_title = models.CharField(max_length=20)
    item_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    item_photo = models.ImageField(null=True, blank=True, upload_to = "items/", default='items/blank.jpg')
    item_quantity = models.IntegerField(default=1)
    item_owner = models.ForeignKey(User, related_name="items_owned", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()


#-----Order Items-----
# refrences a specific item
class OrderItem(models.Model):
    product = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    cart_item = models.ForeignKey(Item, related_name="items_in_cart", on_delete=models.CASCADE)
    users_that_added = models.ManyToManyField(User, related_name="item_user_added")
    cart_quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now=True)

# order consists of many items you buy
class Order(models.Model):
    # on_delete is set to null so if you delete an order, it doesn't delete user
    owner = models.ForeignKey(User, related_name="users_order", on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem, related_name="item_on_order")
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_cart_items(self):
    #     return self.items.all()

    # def get_cart_total(self):
    #     return sum([item.product.price for item in self.items.all()])

    # def __str__(self):
    #     return '{0} - {1}'.format(self.owner)

