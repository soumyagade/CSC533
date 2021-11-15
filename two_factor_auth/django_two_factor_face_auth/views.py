from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserCreationForm, AuthenticationForm, RegisterRhythm
from .authenticate import FaceIdAuthBackend
from .utils import prepare_image
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import io


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/register_face/')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/register.html', context)


def register_face(request):
    return render(request, 'django_two_factor_face_auth/register_face.html')


@csrf_exempt
def register_rhythm(request):
    if request.method == 'POST':
        rhythm_text = request.POST['rhythm_string']
        print(rhythm_text)
        username = "test"
        if username is not None:
            f = open(username + '_rhythm.txt', 'w')
            f.write(rhythm_text)
            f.close()
            print("file saved!")
        return redirect('/accounts/profile/')

    return render(request, 'django_two_factor_face_auth/register_rhythm.html')


def profile(request):
    return HttpResponse("Welcome to your profile page")


def face_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            face_image = prepare_image(form.cleaned_data['image'])

            face_id = FaceIdAuthBackend()
            user = face_id.authenticate(username=username, password=password, face_id=face_image)
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                form.add_error(None, "Username, password or face id didn't match.")
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/login.html', context)
