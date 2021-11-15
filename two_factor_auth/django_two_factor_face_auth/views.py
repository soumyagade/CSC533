from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserCreationForm, AuthenticationForm, RegisterRhythm, CreateUserForm
from .authenticate import FaceIdAuthBackend
from .utils import prepare_image
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import io

########################################################################

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # create the user
            form.save()
            # user = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            return redirect('choose')

    context = {'form' : form}
    return render(request, 'django_two_factor_face_auth/register2.html', context)

def loginPage(request):
    context = {}
    return render(request, 'django_two_factor_face_auth/login2.html', context)

@csrf_exempt
def choose(request):
    context = {}
    return render(request, 'django_two_factor_face_auth/choose.html', context)

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


@csrf_exempt
def register_face(request):

    if request.method == 'POST':
        face = request.FILES['image']
        username = "test"

        with open('faces/' + username + '.png', 'wb+') as destination:
            for chunk in face.chunks():
                destination.write(chunk)

    return render(request, 'django_two_factor_face_auth/register_face.html')


@csrf_exempt
def register_rhythm(request):
    if request.method == 'POST':
        rhythm_text = request.POST['rhythm_string']
        print(rhythm_text)
        username = "test"
        if username is not None:
            f = open('rhythms\\' + username + '.txt', 'w')
            f.write(rhythm_text)
            f.close()
            print("file saved!")
        return redirect('/accounts/profile/')

    return render(request, 'django_two_factor_face_auth/register_rhythm.html')


def profile(request):
    return HttpResponse("Welcome to your profile page")

def home(request):
    return render(request, 'django_two_factor_face_auth/homepage.html')

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

def login_face(request):
    return render(request, 'django_two_factor_face_auth/login_face.html')

def login_rhythm(request):
    return render(request, 'django_two_factor_face_auth/login_rhythm.html')
