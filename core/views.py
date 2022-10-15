from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from files import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404
import os



# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')


def signin(request):
    """
    If the request method is POST, then get the username and password from the request, authenticate the
    user, and if the user is authenticated, then log the user in and render the homepage.html template
    with the user's first name. If the user is not authenticated, then display an error message and
    redirect the user to the home page
    
    :param request: The request object is a Django object that contains metadata about the request sent
    to the server
    :return: The render function is returning a HttpResponse object.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name
            print("Hello succ")
            return render(request, "authentication/homepage.html", {'first_name': first_name})
        else:
            messages.error(request, "Wrong Credentials")
            print("Hello failed")
            return redirect('home')

        print("outside")
    return render(request, 'authentication/signin.html')


"""
    If the request method is POST, create a new post object with the user, file, filename, and
    file_desc, and save it.
        
    :param request: The request object is a Python object that contains all the information about the
    request that was sent to the server
    :return: The redirect function is being returned.
 """
@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        file = request.FILES.get('file')
        filename = request.POST['filename']
        file_desc = request.POST['file_desc']

        new_post = Post.objects.create(user=user, file=file, filename=filename, file_desc=file_desc)
        new_post.save()
        return redirect('homepage')
    else:
        redirect('/')



def signup(request):
    """
    If the request method is POST, then create a new user with the given username, email, password,
    first name, and last name.
    
    :param request: The request is a HttpRequest object. It contains metadata about the request,
    including the HTTP method
    :return: the rendered template.
    """
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
        if len(username) > 10:
            messages.error(request, "username must be under 10 characters")
        if password != password2:
            messages.error(request, "Password didn't match")
        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric")
            return redirect('home')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')

    return render(request, "authentication/signup.html")


    """
    It takes a request, renders the homepage.html template, and passes the feed_list variable to the
    template.
    
    :param request: The request object is the first parameter to all Django views. It contains metadata
    about the request, such as the HTTP method ("GET" or "POST"), the client's IP address, and the query
    parameters
    :return: The request object, the template to be rendered, and the context dictionary.
    """
@login_required(login_url='sigin')    
def homepage(request):
    
    feed_list = Post.objects.all()
    return render(request, "authentication/homepage.html", { 'feed_list':feed_list})



    """
    It deletes the file from the database and then renders the homepage.html template.
    
    :param request: The request object is the first parameter to every view function. It contains
    information about the request that was made to the server, such as the HTTP method, the path, the
    headers, and the body
    :return: The delete_file function is returning the homepage.html template.
    """
@login_required(login_url='signin')    
def delete_file(request):
    feed_list = Post.objects.all()
    feed_list.delete()
    return redirect('homepage')

@login_required(login_url='signin')
def download(request):
    feed_list = Post.objects.all()
    path = feed_list.file.url
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            
    return redirect('homepage')
    


       
@login_required(login_url="signin")
def signout(request):
    logout(request)
    messages.success(request, "Logged out Successfully")
    return redirect('home')
