from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForms


def user_login(request):
    if request.method == "POST":
        form = LoginForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            # print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Success')
                else:
                    return HttpResponse('Error')
            else:
                return HttpResponse('Login va parolda hatolik')
    else:
        form = LoginForms()
        context = {
            'form': form
        }
    return render(request, 'registration/login.html', context)


def dashboard_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'pages/user_profile.html', context)
