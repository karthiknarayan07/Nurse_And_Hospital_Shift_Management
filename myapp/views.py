from django.shortcuts import render,redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import NurseRegistrationForm,HospitalRegistrationForm,LoginForm,shiftCreationForm

from .models import hospitalShiftDetails,AppliedNurses,User

# Create your views here.


def home(request):
    user = None
    is_mediator = None
    if request.user.is_authenticated:
        user=True
        if request.user.is_mediator:
            is_mediator= True

    
    
    allUsers = User.objects.all().exclude(is_mediator=True)
    context={
        "user":user,
        "NurseForm":NurseRegistrationForm(),
        "HospitalForm":HospitalRegistrationForm(),
        "is_mediator":is_mediator,
        "allUsers":allUsers
    }
    return render(request,"home.html",context)

@login_required(login_url="login")
def register_nurse(request):
    if request.user.is_mediator==True:
        if request.method == 'POST':
            NurseForm = NurseRegistrationForm(request.POST)
            if NurseForm.is_valid():
                NurseForm.save()
                return redirect("home")
        
    else:
       return JsonResponse({'status':'nurse registration failed'})

@login_required(login_url="login")
def register_hospital(request):
    if request.user.is_mediator==True:
        if request.method == 'POST':
            HospitalForm = HospitalRegistrationForm(request.POST)

        
            if HospitalForm.is_valid():
                HospitalForm.save()
                return redirect("home")
        
    else:
       return JsonResponse({'status':'Hospital registration failed'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_mediator:
                    return redirect('home')
                elif user.is_hospital:
                    return redirect('hospital')
                elif user.is_nurse:
                    return redirect('nurse')
                else:
                    return redirect('login')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect('home')


#nurse dashboard
@login_required(login_url="login")
def nurse(request):
    if request.user.is_nurse==True:
        if request.method == "POST":

            shiftID = request.POST['shiftID']

            newApplication = AppliedNurses(applicant=request.user,appliedShift=hospitalShiftDetails.objects.get(shiftID=shiftID))
            newApplication.save()

            return redirect("nurse")
        
        else:
            

            
            availableShifts = hospitalShiftDetails.objects.exclude(appliednurses__applicant=request.user).filter(status="open")

            appliedShifts = AppliedNurses.objects.filter(applicant=request.user)
            context={
                "user":request.user,
                "availableShifts":availableShifts,
                "appliedShifts":appliedShifts,
            }
            return render(request,'nurse.html',context)
    else:
        return redirect("home")


#hospital dashboard
@login_required(login_url="login")
def hospital(request):
    if request.user.is_hospital==True:

        if request.method=="POST":
            ShiftCreation =  shiftCreationForm(request.POST)

            if ShiftCreation.is_valid():
                shift = ShiftCreation.save(commit=False)
                shift.hospital = request.user
                shift.save()
                return redirect("hospital")
        else:
            openShifts = hospitalShiftDetails.objects.filter(hospital=request.user).filter(status="open")
            ongoingShifts = hospitalShiftDetails.objects.filter(hospital=request.user).filter(status="closed")
            context={
                "user":request.user,
                "shiftCreationForm":shiftCreationForm(),
                "openShifts":openShifts,
                "ongoingShifts":ongoingShifts,
            }
            return render(request,'hospital.html',context)
    return redirect("home")

@login_required(login_url='login')
def openshifts(request,shiftID):
    if request.user.is_hospital==True:
        if request.method=="POST":
            applicationID = request.POST['applicationID']

            selectedShift = hospitalShiftDetails.objects.get(shiftID=shiftID)
            selectedShift.status="closed"
            selectedShift.save()

            selectedApplicant = AppliedNurses.objects.get(applicationID=applicationID)
            selectedApplicant.is_accepted=True
            selectedApplicant.save()

            return redirect("hospital")
        
        else:
            currentShift = hospitalShiftDetails.objects.filter(status="open").filter(shiftID=shiftID).first()
            applicants= AppliedNurses.objects.filter(appliedShift=shiftID)
            context={
                "currentShift":currentShift,
                "applicants" : applicants,


            }
            return render(request,"openshifts.html",context)
    return redirect('home')

    