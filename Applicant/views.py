from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

import ml


def home(request):
        return render(request, 'index.html')

def registerPage(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request, 'regform.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request, 'regform.html')
            else:

                # save data in db
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'regform.html')
        return redirect('/')
    else:
        return render(request, 'regform.html')


def loginPage(request):
    if request.method == 'POST':
        # v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'predfrom.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'loginform.html')
    else:
        return render(request, 'loginform.html')


def predPage(request):
    if (request.method == 'POST'):
        applicantIncome = request.POST.get('ApplicantIncome','0')
        coAppIncome = request.POST.get('CoapplicantIncome','0')
        maritalStatus = request.POST.get('MaritalStatus')
        gender = request.POST.get('Gender','0')
        dependents = request.POST.get('Dependents','0')
        education = request.POST.get('Education','0')
        empy_type = request.POST.get('Self_Employed','0')
        cred_hist = request.POST.get('Credit_History','0')
        prop_type = request.POST.get('Property_Area','0')
        loanAmount = request.POST.get('LoanAmount','0')
        loanAmountTerm = request.POST.get('Loan_Amount_Term','0')
        #print('DATA = ',int(applicantIncome),coAppIncome,maritalStatus,gender,dependents,education,empy_type,cred_hist,prop_type,loanAmount,loanAmountTerm)
        data = [int(applicantIncome),int(coAppIncome),int(loanAmount),int(loanAmountTerm),int(cred_hist),int(gender == 'Female'),int(gender == 'Male'),int(maritalStatus == 'Unmarried'),
                int(maritalStatus == 'Married'),int(dependents == '0'),int(dependents == '1'),int(dependents == '2'),int(dependents == '3'),
                int(education == 'Graduate'),int(education == 'Not Graduate'),int(empy_type=='Not-Self-employed'),int(empy_type=='Self-employed'),
                int(prop_type=='Rural'),int(prop_type=='Semi-urban'),int(prop_type=='Urban')]
        #print(data)
        #print(sum(data))
        if sum(data) != 1:
            res = ml.output(data)
            if res == "N":
                return render(request,'failure.html')
            elif res == 'Y':
                return render(request,'success.html')
        else:
            return render(request, 'predform.html')
    else:
        return render(request, 'predform.html')

