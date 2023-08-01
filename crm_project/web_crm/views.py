from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUp

def home(request):
    """
    View function for the home page.

    If the request method is POST, attempt to authenticate the user
    with the provided username and password. If successful, log the user
    in, display a success message, and redirect to the 'home' page.
    If authentication fails, display an error message and redirect back
    to the 'home' page.

    :param request: The HTTP request object.
    :return: The rendered 'home.html' template.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Auntheticate
        user = authenticate(request=request,username=username,password=password)
        if user:
             # If authentication is successful, log the user in
            login(request=request,user=user)
            # Display a success message
            print('ok')
            messages.success(request=request,message="You have been logged in")
            return redirect("home")
        else:
            # If authentication fails, display an error message
            messages.error(request=request,message="There was an error, please try again")
            print('no logado')
            return redirect("home")
    return render(request,'home.html',{})



def logout_user(request):
    """
    View function for logging out the user.

    Logs out the authenticated user, displays a success message, and redirects to the 'home' function.

    :param request: The HTTP request object.
    :return: The redirect response to the 'home' function.
    """
    logout(request=request)
    messages.success(request=request,message="You have been logout")
    return redirect("home")



def register_user(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            # Authentication and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request=request,user=user)
            messages.success(request=request,message="Your account was created")
            return redirect('home')
    else:
        form = SignUp()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})


