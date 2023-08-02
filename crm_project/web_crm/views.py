from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Record

from .forms import SignUp


def home(request: HttpRequest) -> HttpResponse:
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


    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Auntheticate
        user = authenticate(request=request, username=username, password=password)
        if user:
            # If authentication is successful, log the user in
            login(request=request, user=user)
            # Display a success message
            print("ok")
            messages.success(request=request, message="You have been logged in")
            return redirect("home")
        else:
            # If authentication fails, display an error message
            messages.error(
                request=request, message="There was an error, please try again"
            )
            print("no logado")
            return redirect("home")
    return render(request, "home.html", {'records':records})


def logout_user(request: HttpRequest) -> HttpResponse:
    """
    View function for logging out the user.

    Logs out the authenticated user, displays a success message, and redirects to the 'home' function.

    :param request: The HTTP request object.
    :return: The redirect response to the 'home' function.
    """
    logout(request=request)
    messages.success(request=request, message="You have been logout")
    return redirect("home")


def register_user(request: HttpRequest) -> HttpResponse:
    """
    View function for registerthe user.

    If the HTTP request method is POST, it processes the SignUp form data, logs in the newly registered user,
    and redirects to the 'home' function after displaying a success message.
    If the method is GET, it renders the 'register.html' template with an empty SignUp form.

    :param request: The HTTP request object.
    :return: The redirect response to the 'home' function or the rendered 'register.html' template.
    """
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            # Authentication and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request=request, user=user)
            messages.success(request=request, message="Your account was created")
            return redirect("home")
    else:
        form = SignUp()
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})


@login_required
def customer_record(request: HttpRequest, pk: int) -> HttpResponse:
    """
    View function for displaying a specific customer record.

    This view retrieves a record identified by the given 'pk' (primary key)
    and renders the 'record.html' template with the record data, allowing
    the user to view the details of the record. If the record with the
    specified primary key does not exist, an error message will be shown,
    and the user will be redirected to the 'home' page.

    :param request: The HTTP request object.
    :param pk: The primary key of the record to display.
    :return: The rendered 'record.html' template with the record data or
             a redirect response to the 'home' function if the record does
             not exist.
    """
    try:
        record = get_object_or_404(Record, id=pk)
        return render(request, 'record.html', {'customer_record': record})
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect('home')
    

@login_required
def delete_record(request: HttpRequest,pk: int) -> HttpResponse:
    """
    Delete a specific record identified by 'pk'.

    If the user is authenticated and the record exists, it will be deleted.
    A success message will be displayed upon successful deletion, and the user
    will be redirected to the 'home' page. If the record does not exist, an error
    message will be shown, and the user will be redirected to the 'home' page.

    :param request: The HTTP request object.
    :param pk: The primary key of the record to delete.
    :return: Redirect response to the 'home' function.
    """
    try:
        customer_record = get_object_or_404(Record, id=pk)
        customer_record.delete()
        messages.success(request, "Record deleted")
        return redirect('home')
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect('home')