from django.shortcuts import render,redirect
from .models import *
import bcrypt

from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request,'index.html')


def register(request):
    error = False
# length validations - to avoid blank fields
    if len(request.POST['first_name']) < 2:
        messages.error(request,'First name must be at least 2 characters')
        error = True
# to avoid names containing any numbers
    elif not request.POST['first_name'].isalpha():
        messages.error(request,'First name cannot contain any numbers')
        error = True
    if len(request.POST['last_name']) < 2:
        messages.error(request,'Last name must be at least 2 characters')
        error = True
    elif not request.POST['last_name'].isalpha():
        messages.error(request,'Last name cannot contain any numbers')
        error = True
    if len(request.POST['email']) < 2:
        messages.error(request, 'Email cannot be blank')
# EMAIL_REGEXT to validate format of the email - must (import re and include format)
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Must be a valid email')
        error = True
# Check if the user already exists
    if User.objects.filter(email = request.POST['email']):
        messages.error(request, 'User already exists')
        error = True
    if len(request.POST['password']) < 8:
        messages.error(request,'Password must be at least 8 characters in length')
        error = True
    if request.POST['c_password'] != request.POST['password']:
        messages.error(request,'Passwords must match!')
        error = True
    if error:
        messages.error(request,'Try again!')
        return redirect('/')
    
    hashed =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    decoded_hash = hashed.decode('utf-8')
    
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = decoded_hash)

    request.session['user_id'] = user.id
    print('User was created')

    return redirect('/dashboard')

def login(request):
    error = False
    
    if len(request.POST['email']) < 2:
        error = True
        messages.error(request, 'Email cannot be blank')

    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Must be a valid email')
        error = True
    if len(request.POST['password']) < 2:
        messages.error(request,"Password cannot be blank")
    
    if error:
        messages.error(request,'Invalid credentials')
        return redirect('/')
# ************************************************************************
    user_list = User.objects.filter(email = request.POST['email'])
    
    if not user_list:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')
    
    user = user_list[0]
    
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        print('You are logged in!')
        return redirect('/dashboard')
    
    else:
        messages.error(request, "Invalid Credentials")
        return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dash(request):
    if not 'user_id' in request.session:
        return redirect('/')
    
    user = User.objects.get(id = request.session['user_id'])
    
    context ={
        'jobs' : Job.objects.all(),
        'user': User.objects.get(id = user.id),
        'my_jobs': Job.objects.filter(creator_id = user)

    }
    return render(request,'dashboard.html', context)

def description(request,id):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context ={
        'user': User.objects.get(id = user.id),
        'job': Job.objects.get(id = id),
    }
    return render(request, 'description.html', context)

def edit(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user' : User.objects.get(id = user.id),
        'job' : Job.objects.get(id = id)
    }

    return render(request, 'edit.html',context)

def update(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    
    user = User.objects.get(id = request.session['user_id'])
    error = False
    
    if len(request.POST['title']) < 4:
        messages.error(request, 'Title must be at least 3 characters in length')
        error = True
    if len(request.POST['description']) < 4:
        messages.error(request, 'Description must be at least 3 characters in length')
        error = True
    if len(request.POST['location']) < 4:
        messages.error(request, 'Location must be at least 3 characters in length')
        error = True
    if error:
        messages.error(request, 'Invalid Edit')
        return redirect ('/edit/' + str(id))
    
    job = Job.objects.get(id = id)
    
    job.title = request.POST['title']
   
    
    job.description =  request.POST['description']

    
    job.location = request.POST['location']
    job.save()
    
    messages.error(request, 'You have successfully edited your job!')
    
    return redirect('/edit/' +str(id))

def delete(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    
    Job.objects.get(id = id).delete()
    return redirect ('/dashboard')

def add(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])

    context = {
        'user': User.objects.get(id = user.id)
    }
    return render(request,'add_job.html',context)

def create(request):
    if not 'user_id' in request.session:
        return redirect('/')
    
    user = User.objects.get(id = request.session['user_id'])
    
    error = False
    
    if len(request.POST['title']) < 4:
        messages.error(request, 'Title must be at least 3 characters in length')
        error = True
    if len(request.POST['description']) < 4:
        messages.error(request, 'Description must be at least 3 characters in length')
        error = True
    if len(request.POST['location']) < 4:
        messages.error(request, 'Location must be at least 3 characters in length')
        error = True
    if error:
        messages.error(request, 'Invalid Edit')
        return redirect ('/add')
    
    Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'], creator = user)

    messages.error(request, 'You have successfully created a new job!')
    return redirect ('/dashboard')


