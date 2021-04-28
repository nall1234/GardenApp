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
    return render(request, 'main.html')

# -----MARKETPLACE-----
def market(request):
    if 'current_user' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['current_user']),
        'all_items': Item.objects.all()
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


#-----MY CART-----
def my_cart(request):
    return render(request, 'cart.html')

#-----ADD TO CART-----
def add_cart(request):
    # if 'current_user' not in request.session:
    #     return redirect('/')
    # if request.method =="POST":
    #     # get user object
    #     user = User.objects.get(id= request.session['current_user'])
    #     # get item id
    #     item = Item.object.filter(id=item_id.get.first())
    #     # create OrderItem 
    #     order_item = OrderItem.objects.get_or_create(item=item)
    #     # create Order associated with user
    #     user_order = Order.objects.get_or_create(owner=user_profile)
    #     # adding OrderItem to user_order.items.add(order_item)
    #     user_order.items.add(order_item)
    #     # save user_order
    #     user_order.save()
    # return redirect(request, '/market')
    pass


# ------Add Cart Code from 4/27 session (Evan & Caitlyn)-----
        #  establish user 
        # user = User.objects.get(id= request.session['current_user'])
        # new_item = OrderItem.objects.create(cart_item=request.POST['cart_item'], cart_quantity=request.POST['cart_quantity'], users_that_added=user)
        # #establish if there is an order open 
        # current_orders = User.order.filter(is_ordered=False)
        # one_order = current_orders[0]
        # if one_order:
        #     if one_order.items.filter(items.order_item.item.id = request.POST['cart_item.id']new_item.item.id):
        #         item.quantity = item.quantity+new_item.quantity
        #     else:
        #         one_order.items.add(new_item)
        # return redirect('/market')


        # if an order is open, first check to see if item is already in cart, if not then create order item
        # add to cart 
        # else, add to quantity on order
        # then create order item 
        # add to cart 
        # item = Item.objects.create(item_title=request.POST['item_title'], item_description=request.POST['item_description'], price= request.POST['product_id'], item_photo= request.FILES['item_photo'], item_quantity=request.POST['item_quantity'], item_owner = User.objects.get(id=request.session['current_user']))
        # request.session['item_id'] = item.id
        # messages.success(request, "Item created")
        # return redirect('/market')


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
