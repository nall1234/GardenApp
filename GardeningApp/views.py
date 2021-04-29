from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    if 'current_user' in request.session:
        return redirect ('/main')
    return render (request, 'index.html')

def login(request):
    if request.method == "POST":   
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        current_user = User.objects.get(email = request.POST['email'])
        request.session['current_user'] = current_user.id
        return redirect('/main')            
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def register(request):
    if request.method =="POST":
        errors = User.objects.user_validator(request.POST)        
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pwhash
        )
        request.session['current_user'] = new_user.id
        return redirect('/main')
    else:
        return redirect("/")

def main(request):
    user = User.objects.get(id=request.session['current_user'])
    context = {
        "user": user,
        "image": user.image
    }
    return render(request, 'main.html', context)

def profile(request, current_user):
    user = User.objects.get(id=request.session['current_user'])
    context = {
        "user": user,
        "image": user.image
    }
    return render(request, 'profile.html', context)

def update(request, current_user):
    # errors = User.objects.edit_validator(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('update', current_user=current_user)
    # else:
    user = User.objects.get(id=request.session['current_user'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.image = request.FILES['image']
    user.save()
    return redirect('profile', current_user=current_user)

# -----MARKETPLACE-----
def market(request):
    if 'current_user' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['current_user'])
    context = {
        "items" : Item.objects.all(),
        "user": user,
        "image": user.image
    }
    return render(request, 'marketplace.html', context)

#-----CREATE ITEM POST-----
def create_item(request):
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Item.objects.item_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/market')
        else:
            item = Item.objects.create(item_title=request.POST['item_title'], item_description=request.POST['item_description'], price= request.POST['product_id'], item_photo= request.FILES['item_photo'], item_quantity=request.POST['item_quantity'], item_owner = User.objects.get(id=request.session['current_user']))
            request.session['item_id'] = item.id
            messages.success(request, "Item created")
            return redirect('/market')
    return redirect('/market')


#-----VIEW ONE IEM POST-----
def one_item(request, item_id):
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method =="GET":
        context = {
            'one_item': Item.objects.get(id=item_id)
        }
    return render(request, 'one_item.html', context)

#-----EDIT ONE ITEM-----
def edit_item(request, item_id):
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method =="GET":
        context = {
            'one_item': Item.objects.get(id=item_id)
        }
    return render(request, "edit_item.html", context)


#-----UPDATE ITEM-----
def update_item(request, item_id):
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method =="POST":
        item_to_update = Item.objects.get(id=item_id)
        item_to_update.item_title = request.POST['item_title']
        item_to_update.item_description = request.POST['item_description']
        item_to_update.product_id = request.POST['product_id']
        item_to_update.item_photo = request.FILES['item_photo']
        item_to_update.save()
    return redirect('/market')

#-----DELETE ITEM-----
def delete_item(request, item_id):
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method == "POST":
        item_to_delete = Item.objects.get(id=item_id)
        if item_to_delete.item_owner.id == request.session['current_user']:
            item_to_delete.delete()
    return redirect('/market')


def my_cart(request):
    user =  User.objects.get(id= request.session['current_user'])
    all_orders = user.users_order.filter(is_ordered = False)
    order = all_orders[0]
    context = {
        'user' : user,
        "order_items" : order.items.all()
    }
    return render(request, 'cart.html', context)

#-----ADD TO CART-----
def add_cart(request, item_id):    
    if 'current_user' not in request.session:
        return redirect('/')
    if request.method =="POST":
    #     # get user object
        user = User.objects.get(id= request.session['current_user'])
        #   # get item id
        quantity = request.POST['item_quantity']
        item = Item.objects.get(id = item_id)
        order_item = OrderItem.objects.create(
            cart_item= item,
            users_that_added = user,
            cart_quantity = request.POST['item_quantity'],
        )        
        all_orders = user.users_order.filter(is_ordered = False)
        if all_orders:
            current_order = all_orders[0]
            if current_order.items.filter(cart_item = item):
                current_item = current_order.items.get(cart_item = item)
                current_item.cart_quantity = int(current_item.cart_quantity) + int(quantity)
                current_item.save()
                return redirect('/market')
            else:
                current_order.items.add(order_item)
        else:
            new_order = Order.objects.create(
                owner = user
            )
            new_order.items.add(order_item)
            new_order.save()    
    return redirect('/market')



#-----REMOVE FROM CART-----
def remove_cart(request, item_id):
    # item_to_delete = OrderItem.objects.filter(id=item_id)
    # if item_to_delete.exists():
    #     item_to_delete[0].delete()
    # return redirect(request, '/market/cart')
    pass

#-----CHECKOUT-----
def checkout(request):
    pass


# message board views 

def community(request):
    if  'current_user' not in request.session:
        return redirect("/")
    else:        
        context = {
            "user" : User.objects.get(id = request.session['current_user']),
            'messages': Message.objects.all(),
            'comments': Comment.objects.all(),
        }
    return render(request, 'community.html', context)

def add_message(request):
    user = User.objects.get(id= request.session['current_user'])
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/community')
    Message.objects.create(
        message = request.POST['message'],
        message_creator = User.objects.get(id= request.session['current_user'])
    )
    return redirect('/community')


def delete_message(request, message_id):
    message = Message.objects.get(id= message_id)
    message.delete()
    return redirect('/community')

def add_comment(request, id):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/community')
    Comment.objects.create(
        comment = request.POST['comment'],
        comment_message = Message.objects.get(id =id),
        comment_creator = User.objects.get(id=request.session['current_user'])
    )
    return redirect('/community')

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id= comment_id)
    comment.delete()
    return redirect('/community')
