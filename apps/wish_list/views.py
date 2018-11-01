from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import re
import bcrypt
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	return render(request, 'wish_list/index.html')

def registration(request):
	errors = []
	if len(request.POST['first_name']) < 2:
		errors.append("First name must be at least 2 characters")
	if len(request.POST['alias']) < 2:
		errors.append("Alias name must be at least 2 characters")
	if len(request.POST['password']) < 8:
		errors.append("Password must be at least 8 characters")
	if request.POST['password'] != request.POST['confirm']:
		errors.append("Password and password confirmation don't match. Try again!")
	if request.POST['date']=='':  #ask a question
		
		errors.append("PLease enter Date")
	if not EMAIL_REGEX.match(request.POST['email']):
		messages.error(request,"Invalid Email")
            
	if errors:
		for err in errors:
			messages.error(request, err)
			print(errors)
		return redirect('/')
	
	else:	
		try:
			User.objects.get(email=request.POST['email'])
			messages.error(request, "User with that email already exists.")
			return redirect('/')
		except User.DoesNotExist:
			hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(first_name=request.POST['first_name'],\
									alias=request.POST['alias'],\
									password = hashpw,\
                                    date=request.POST['date'],\
									email = request.POST['email'])
			request.session['message'] = "You are registered"
			request.session['user_id'] = user.id
			return redirect('/dashboard')

def login(request):
	try:
		user = User.objects.get(email = request.POST['email'])

		if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
			request.session['user_id'] = user.id
			request.session['message'] = "You are logged in"
			return redirect('/dashboard')
		else:
			messages.error(request, 'Email or password are incorrect')
			return redirect('/')
	except User.DoesNotExist:
		messages.error(request, "Email doesn't exist.")
		return redirect('/')
def logout(request):
	request.session.clear()
	return redirect('/')


def dashboard(request):
    products=Product.objects.exclude(favorites=request.session['user_id'])
    wishlists=Product.objects.filter(favorites=request.session['user_id'])
    allproducts=Product.objects.all()
    context={
        'login_user':User.objects.get(id=request.session['user_id']),
        'allusers':User.objects.all(),
        'allproducts':allproducts,
        'wishlists':wishlists,
        'products':products

    }
    return render(request, 'wish_list/dashboard.html',context)
def create(request):

   
    


    return render(request, 'wish_list/create.html')

def additem(request):
    errors = []
    if len(request.POST['name']) < 3:
        messages.error(request, 'Item name must be at least 3 characters')
        return redirect('wish_items/create')

    if errors:
        for err in errors:
            messages.error(request, err)
        return redirect('wish_items/create')

    
    else:
        
        Product.objects.create(name=request.POST['name'], user=User.objects.get(id=request.session['user_id']))
    
        return redirect('/dashboard')
def addwishlist(request):
    m=Product.objects.get(id=request.POST['productid'])
    m.favorites.add(request.session['user_id'])
    m.save()
    return redirect('/dashboard')

def removefromlist(request):
    m=Product.objects.get(id=request.POST['productid'])
    m.favorites.remove(User.objects.get(id=request.session['user_id']))
    m.save()
    return redirect('/dashboard')

def show_item(request,id):
    product=Product.objects.get(id=id)

  
    context={
        'product':product,
    }
    return render(request, 'wish_list/show_item.html',context)