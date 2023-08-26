from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddRecordForm, SignUp
from .models import Record


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
    return render(request, "home.html", {"records": records})


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
        return render(request, "record.html", {"customer_record": record})
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect("home")


@login_required
def delete_record(request: HttpRequest, pk: int) -> HttpResponse:
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
        return redirect("home")
    except Record.DoesNotExist:
        messages.error(request, "Record not found.")
        return redirect("home")


@login_required
def add_record(request: HttpRequest) -> HttpResponse:
    """
    Add a new record to the database.

    If the user is authenticated, this view processes the information submitted via the 'add_record.html' form
    to create a new record in the database. Upon successful addition, a success message will be displayed,
    and the user will be redirected to the 'home' page.
    If the form data is invalid, an error message will be shown,and the user will be redirected to the 'home' page.

    :param request: The HTTP request object.
    :return: Redirect response to the 'home' function or rendering of the 'add_record.html' template.
    """
    form = AddRecordForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Record Added")
            return redirect("home")
        else:
            messages.error(request, "You Must Be Logged In To Do That...")
            return redirect("home")
    return render(request, "add_record.html", {"form": form})


@login_required
def update_record(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Update a specific record identified by 'pk'.

    This view allows an authenticated user to update a record.
    If the record exists and the user successfully updates it,
    they are redirected to the 'home' page with a success message.
    If the record doesn't exist, an error message is shown,
    and the user is redirected to the 'home' page.

    :param request: The HTTP request object.
    :param pk: The primary key of the record to update.
    :return: Redirect response to the 'home' function.
    """
    current_record = get_object_or_404(Record, id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect("home")
        else:
            messages.error(request, "Invalid form data. Please correct the errors.")
            return redirect("home")
    else:
        form = AddRecordForm(instance=current_record)
        return render(request, "update_record.html", {"form": form})
