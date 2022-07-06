from django.shortcuts import get_object_or_404, redirect,render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.utils import timezone
import subprocess,os,sys
from django.contrib.auth.forms import UserCreationForm
import os.path
from .models import Problem,Testcase,Submission
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login as auth_login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

#@login_required(login_url='practice:login')
def index(request):
    Problem_list = Problem.objects.order_by('problemid')
    context = {'Problem_list': Problem_list}
    return render(request, 'practice/index.html', context)

@login_required(login_url='practice:login')
def detail(request, problemid):
    problem = get_object_or_404(Problem, pk=problemid)
    return render(request, 'practice/detail.html', {'problem': problem})

def login(request):
    if request.user.is_authenticated:
        return redirect('practice:home')
    
    else:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('practice:index')

            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'practice/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('practice:home')
    
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('practice:login')

        context = {'form':form}
        return render(request, 'practice/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('practice:login')

@login_required(login_url='practice:login')
def leaderboard(request):
    recent_submissions = Submission.objects.all().order_by('-submissiontime')[:10]
    return render(request, 'practice/leaderboard.html', {"solutions": recent_submissions})

def submit(request, problemid):
    input=Testcase.objects.get(pk=problemid).inputdoc
    output=Testcase.objects.get(pk=problemid).outputdoc
  
#We can Store the submitted file in this path with dynamic name (problemid)
    temp = r"D:\abhigyan\Documents\Projects\Online-coding-Judge\submissions\%s"%problemid + ".cpp" 
    
    #creating the submission file
    code_file=open(temp,'wb+') 


    code=request.POST.get('code')
    #we need to convert the code that we get from form to bytes to use the write command
    code=bytes(code,'utf-8')
    code_file.write(code)
    
    #now in the submission file the text is copied from code , we need to convert it to bytes to allow subprocess to run it
    code_file=bytes(temp,'utf-8')
    
    
    #if there is a problem while compiling we set the verdict as compilation error
    compile=subprocess.run(["g++",temp],shell=True)
    verdict=""

    if(compile.returncode!=0):
        verdict="Compilation Error"

    expected_output=open(output,'r').read()

    input_file=open(input,'r')

    process = subprocess.run('a.exe', stdin=input_file,shell=True, capture_output=True,text=True)
     
    
    user_output= process.stdout.strip()


    # we need to check if there was a problem in compiling the submitted code as even after compilation error there might be previous "a.exe" file of previous code available in the system
    if(process.returncode!=0 ):
        verdict="Compilation Error"
    elif(expected_output==user_output and verdict!="Compilation Error"):
        verdict="Answer Correct"
    elif(verdict!="Compilation Error"):
        verdict="Wrong answer"
    
    submission=Submission()
    temp=str(temp)

    submission.problemid=Problem.objects.get(pk=problemid)
    submission.answercode=temp
    submission.verdict=verdict
    submission.save()

    
    # return HttpResponse("Your Anwer verdict is %s." % verdict)
    return redirect('practice:leaderboard')


    
    


    
