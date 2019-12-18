from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse


def get_success_url(request):
    """
    Funkcja wykorzystywana do redirect.
    Po zalogowaniu akcja wraca do widoku, który był wcześniej realizowany
    """
    next_url = request.GET.get('next', None)
    if next_url:
        return "%s" % next_url  # you can include some query strings as well
    else:
        return reverse('shop:index')  # what url you wish to return


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user, created = User.objects.get_or_create(username=username, is_staff=True)
            user.set_password(password)
            user.save()

            return redirect('shop:index')

    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'login_system/register.html', context)


def my_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(get_success_url(request))

    form = AuthenticationForm()
    return render(request, 'login_system/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('shop:index')
