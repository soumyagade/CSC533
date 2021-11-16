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
from .models import UserProfile, UserFaceImage
from django.contrib.auth.models import User
import io
from os.path import exists

########################################################################

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # create the user
            user = form.save()
            userName = form.cleaned_data.get('username')
            # messages.success(request, 'Account was created for ' + user)
            UserProfile.objects.create(user=user, home_address="7217 Starcross Ct")
            return redirect('/choose/' + '?username='+userName)

    context = {'form' : form}
    return render(request, 'django_two_factor_face_auth/register2.html', context)

def loginPage(request):
    context = {}
    return render(request, 'django_two_factor_face_auth/login2.html', context)

@csrf_exempt
def registerFacePage(request):
    if request.method == 'POST':
        face = request.FILES['image']
        username = request.POST['username']
        uid = User.objects.get(username=username)
        face_image = UserFaceImage(user=uid, image=face)
        face_image.save()
        # UserProfile.objects.filter(user=uid).update(image=face)
    return render(request, 'django_two_factor_face_auth/register_face.html')

########################################################################

@csrf_exempt
def login_face(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # print("USERNAME: " + username)
        password = request.POST.get('password')
        # print("PASSWORD: " + password)
        face_image = request.FILES['image']
        face_id = FaceIdAuthBackend()
        user = face_id.authenticate(username=username, password=password, face_id=face_image)
        if user is not None:
            # print("FOUND A USER")
            login(request, user)
            return HttpResponse("SUCCESS")
        else:
            return HttpResponse("FAILURE")

        # username = request.POST['username']
        # compare_face = False
        # if username != "undefined" and username != "":
            # TODO: Add logic to actually compare the faces here
            # compare_face = True
        # if compare_face:
            # return HttpResponse("SUCCESS")
        # else:
            # return HttpResponse("FAILURE")
    context = {}
    return render(request, 'django_two_factor_face_auth/login_face.html', context)

@csrf_exempt
def face_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # print("USERNAME: " + username)
        password = request.POST.get('password')
        # print("PASSWORD: " + password)
        face_image = request.FILES['image']
        face_id = FaceIdAuthBackend()
        user = face_id.authenticate(username=username, password=password, face_id=face_image)
        if user is not None:
            print("FOUND A USER")
            login(request, user)
            return redirect('/accounts/home')

    context = {}
    return render(request, 'django_two_factor_face_auth/login.html', context)

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
        username = request.POST['username']
        if username != "":
            with open('faces/' + username + '.png', 'wb+') as destination:
                for chunk in face.chunks():
                    destination.write(chunk)

    return render(request, 'django_two_factor_face_auth/register_face.html')


@csrf_exempt
def register_rhythm(request):
    if request.method == 'POST':
        rhythm_text = request.POST['rhythm_string']
        print(rhythm_text)
        username = request.POST['username']
        if username is not None and username != "":
            f = open('rhythms/' + username + '.txt', 'w')
            f.write(rhythm_text)
            f.close()
            print("file saved!")
        return redirect('/accounts/profile/')

    return render(request, 'django_two_factor_face_auth/register_rhythm.html')


def profile(request):
    return HttpResponse("Welcome to your profile page")

def home(request):
    return render(request, 'django_two_factor_face_auth/homepage.html')
    context = {'form': form}
    return render(request, 'django_two_factor_face_auth/login.html', context)


def check_rhythm(list1, list2, threshold):
    """
    Checks if 2 different rhythms match. Rhythms should be passed as a list of integers, where each integer
    represents the time in ms a button was held down or the gaps between presses.
    e.g [500, 1000, 500] would indicate the button was pressed for half a second, then the user waited for 1 second,
    then it was pressed for half a second again.

    :param list1: A rhythm represented in a python list
    :param list2: A different rhythm
    :param threshold: The maximum percent difference that can exist between two parts of a rhythm
    :return: True if the rhythms match, false otherwise
    """
    if len(list1) != len(list2):
        return False

    for i in range(len(list1)):
        if abs((list1[i] - list2[i]) / list1[i]) > threshold and abs(list1[i] - list2[i]) > 50:
            return False

    return True

@csrf_exempt
def login_rhythm(request):
    if request.method == 'POST':
        rhythm_string = request.POST['rhythm_string']
        username = request.POST['username']
        password = request.POST['password']
        compare_rhythm = False

        user = authenticate(username=username, password=password)

        if user is not None:
            if exists("rhythms/" + username + ".txt"):
                f = open("rhythms/" + username + ".txt")
                old_rhythm = list(map(int, f.read()[1:-1].split(',')))
                new_rhythm = list(map(int, rhythm_string[1:-1].split(',')))

                f.close()

                compare_rhythm = check_rhythm(old_rhythm, new_rhythm, .5)

        print("USERNAME: " + username)
        if compare_rhythm:
            return HttpResponse("SUCCESS")
        else:
            return HttpResponse("FAILURE")
    return render(request, 'django_two_factor_face_auth/login_rhythm.html')


