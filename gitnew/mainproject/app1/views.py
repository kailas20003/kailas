from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import *
import razorpay
from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore
# Create your views here.
def index(request):
    return render(request,'index.html')
def doctor(request):
    data = add_doctor.objects.all()
    return render(request, 'doctor.html', {'data': data})


def about(request):
    return render(request,'about.html')
def contact(request):
    if 'user' in request.session:
        s=sign_up.objects.get(username=request.session['user'])
        if request.method == 'POST':
            d = request.POST['n4']
            contact1.objects.create(user_details=s,message=d).save()
            return redirect(contact)
        return render(request,'contact.html',{'data':s})
    else:
        return redirect(login)

from datetime import datetime
def appointment(request):
    data = add_doctor.objects.all()
    if 'user' in request.session:
        s=sign_up.objects.get(username=request.session['user'])
        #
        if request.method == 'POST':
            d = request.POST['inputSymptoms']
            e = request.POST['service_date']
            f = request.POST['inputDoctorName']
            print(f)
            request.session['inputSymptoms']=d
            request.session['service_date']=e
            request.session['inputDoctorName']=f
            # f = request.POST['service_end_time']
            # start_time_str = 'service_end_time'.split(' - ')[0]
            t = add_doctor.objects.get(doctorname=f)
            print(t)
            # Convert start_time_str to a valid time format (HH:MM)
            # try:
            #     appointment_time = datetime.strptime(start_time_str, "%H:%M").time()  # Convert to time object
            # except ValueError:
            #     # Handle the error if the time format is invalid
            #     print("Invalid time format")
            #     return render(request, 'appointment.html', {'data': data, 's': s, 'error': "Invalid time format"})

            print(d,e,)
            return redirect(payment)
        # user = sign_up.objects.get(username=request.session['user'])
        return render(request, 'appointment.html', {'data': data,'s':s})
    else:
        return redirect(login)
def treatment(request):
    data = add_treatment.objects.all()
    return render(request, 'treatment.html', {'data': data})


def signup(request):
    if request.method == 'POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        if sign_up.objects.filter(username=a).exists():
            messages.error(request,'username already exists')
            return render(request,'signup.html')
        else:
            if d==e:
                sign_up.objects.create(username=a, email=b,phone=c,password=d).save()
                messages.success(request, 'signup successfully')
                return render(request,'login.html')
            else:
                messages.error(request,'password is not match')
                return render(request,'signup.html')
    return render(request, 'signup.html')
def adminhome(request):
    return render(request,'adminhome.html')
def userhome(request):
    return render(request,'userhome.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import sign_up  # Ensure that this import is correct

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import sign_up, add_doctor  # Import both models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password # Import password checking utility

def login(request):
    if request.method == 'POST':
        u = request.POST['n1']  # Get the username from the form
        p = request.POST['n2']  # Get the password from the form
        print(u,p)
        # Check if the user is a regular user or admin in the sign_up model
        try:
            user = sign_up.objects.get(username=u)
            print(user)
            if user.password == p:  # Direct password comparison (secure with hashing in production)
                request.session['user'] = u  # Store the session
                print("hai")
                return redirect(userhome)  # Redirect to user home

                # Check if the user is an admin or regular user

            else:
                print("userr")
                return HttpResponse("Invalid username or password")

        except sign_up.DoesNotExist:
            # If the user is not found in sign_up, check if they are a doctor in add_doctor
            try:
                doctor = add_doctor.objects.get(doctorusername=u)
                if doctor.doctorpassword == p:  # Direct password comparison
                    request.session['doctor'] = u  # Store the session for doctor
                    return redirect('doctorhome')  # Redirect to doctor home
                else:
                    print("doctorr")
                    return HttpResponse("Invalid username or password")

            except add_doctor.DoesNotExist:
                if u == 'kailas' and p == 'kailas123':  # You can check the role here if you add a 'role' field
                        print("hello")
                        request.session['admin'] = u
                        return redirect(adminhome)  # Redirect to admin home
                else:
                    print("adminnn")
                    # If the username is not found in either model, show an error
                    return HttpResponse("Invalid username or password")

    return render(request, 'login.html')  # Render the login form if not a POST request

def logout(request):
    if 'user' in request.session or 'admin' in request.session:
        request.session.flush()
        return redirect(index)
    return redirect(index)


def treatment2(request):
    data = add_treatment.objects.all()
    return render(request, 'treatment2.html', {'data': data})


def doctor2(request):
    data = add_doctor.objects.all()
    return render(request, 'doctor2.html',{'data':data})

def addtreatment(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.POST['n1']
            b = request.POST['n2']
            c = request.FILES['n3']
            add_treatment.objects.create(treatmentname=a,about=b,logo=c).save()
            return HttpResponse('saved')
        return render(request, 'addtreatment.html')
    else:
        return redirect(login)

def adddoctor(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            a = request.POST['n1']
            b = request.POST['n2']
            c = request.POST['n3']
            d = request.FILES['n5']
            e = request.POST['n6']
            f = request.POST['n7']
            add_doctor.objects.create(doctorname=a,phoneno=b,department=c,image=d,doctorusername=e,doctorpassword=f).save()
            messages.success(request, 'added successfully')
        return render(request, 'adddoctor.html')
    else:
        return redirect(login)

def message(request):
    data = contact1.objects.all()
    return render(request, 'message.html', {'data': data})
def managedoctor(request):
    data = add_doctor.objects.all()
    return render(request, 'managedoctor.html',{'data':data})

def managetreatment(request):
    data = add_treatment.objects.all()
    return render(request,'managetreatment.html',{'data':data})

# def update(request,d):
#     data=add_doctor.objects.get(pk=d)
#     if request.method=='POST':
#         a=request.POST['n1']
#         b = request.POST['n2']
#         c = request.POST['n3']
#         add_doctor.objects.filter(pk=d).update(doctorname=a,phoneno=b,department=c)
#         messages.success(request, 'updated successfully')
#     return render(request, 'update.html',{'data':data})

def normal(request):
    n=normal_form()
    if request.method=='POST':
        n=normal_form(request.POST,request.FILES)
        if n.is_valid():
            a=n.cleaned_data['product_name']
            b = n.cleaned_data['product_price']
            c = n.cleaned_data['product_quantity']
            d = n.cleaned_data['product_image']
            add_doctor.objects.create(doctorname=a,phoneno=b,department=c,image=d).save()
            return HttpResponse("saved")
    return render(request,'form.html',{'data':n})

def modelform(request):
    m=model_form()
    if request.method=='POST':
        m=model_form(request.POST,request.FILES)
        if m.is_valid():
            m.save()
            return HttpResponse("saved")
    return render(request,'form.html',{'data':m})

def update_form(request,d):
    data=add_doctor.objects.get(pk=d)
    m = model_form(instance=data)
    if request.method == 'POST':
        m = model_form(request.POST, request.FILES,instance=data)
        if m.is_valid():
            m.save()
            messages.success(request, 'updated successfully')
    return render(request, 'update.html', {'data': m})

def delete_doctor(request,d):
    data=add_doctor.objects.get(pk=d)
    print(data)
    data.delete()
    return redirect(managedoctor)

def delete_message(request,d):
    data=contact1.objects.get(pk=d)
    print(data)
    data.delete()
    return redirect(message)


def doctorhome(request):
    return render(request,'doctorhome.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import appointment1

from django.shortcuts import get_object_or_404, redirect, render
from .models import appointment1, add_doctor

from django.shortcuts import render, redirect, get_object_or_404
from .models import appointment1


def appointmentapprove(request):
    if 'doctor' in request.session:
        d = add_doctor.objects.get(doctorusername=request.session['doctor'])
        appointments = appointment1.objects.filter(appointment_doctor_details=d).exclude(status='rejected')

        if request.method == "POST":
            appointment_id = request.POST.get('appointment_id')
            action = request.POST.get('action')
            appointment = get_object_or_404(appointment1, id=appointment_id)

            if action == 'approve':
                appointment.status = 'approved'
                appointment.appointment_time = request.POST.get('appointment_time')
            elif action == 'reject':
                appointment.status = 'rejected'

            appointment.save()
            return redirect('appointmentapprove')

        return render(request, 'appointmentapprove.html', {'data': appointments})
    else:
        return redirect('login')


def set_time_slot(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        appointment_time = request.POST.get('appointment_time')

        appointment = get_object_or_404(appointment1, id=appointment_id)

        # Set the time slot for the appointment
        appointment.appointment_time = appointment_time
        appointment.save()

        return redirect('appointmentapprove')  # Redirect back to the appointment approval page
    else:
        return redirect('appointmentapprove')  # In case of invalid request


from django.shortcuts import render, redirect
from .models import add_doctor

def doctorprofile(request):
    # Ensure the user is logged in as a doctor
    if 'doctor' in request.session:
        # Get the current doctor from the session
        s = add_doctor.objects.get(doctorusername=request.session['doctor'])
        return render(request, 'doctorprofile.html', {'s': s})
    else:
        return redirect('login')  # Redirect to login if not logged in as a doctor



def normal2(request):
    n=normal_form2()
    if request.method=='POST':
        n=normal_form2(request.POST,request.FILES)
        if n.is_valid():
            a=n.cleaned_data['treatmentname']
            b = n.cleaned_data['about']
            c = n.cleaned_data['logo']
            add_doctor.objects.create(treatmentname=a,about=b,logo=c).save()
            return HttpResponse("saved")
    return render(request,'form2.html',{'data':n})


# def modelform2(request):
#     m=model_form()
#     if request.method=='POST':
#         m=model_form2(request.POST,request.FILES)
#         if m.is_valid():
#             m.save()
#             return HttpResponse("saved")
#     return render(request,'form2.html',{'data':m})

def update_form2(request,d):
    data=add_treatment.objects.get(pk=d)
    m = model_form2(instance=data)
    if request.method == 'POST':
        m = model_form2(request.POST, request.FILES,instance=data)
        if m.is_valid():
            m.save()
            messages.success(request, 'updated successfully')
    return render(request, 'updatetreatment.html', {'data': m})

def delete_treatment(request,d):
    data=add_treatment.objects.get(pk=d)
    print(data)
    data.delete()
    return redirect(managetreatment)


def myappointment(request):
    if 'user' in request.session:
        # Get the current logged-in user from the session
        user = sign_up.objects.get(username=request.session['user'])

        # Fetch all appointments for the logged-in user
        data = appointment1.objects.filter(appointment_user_details=user)

        return render(request, 'myappointment.html', {'data': data})
    else:
        return redirect('login')  # Ensure the redirect is to the correct login page

def payment(request):
    amount=5
    total_amount = amount*100
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        # cursor = connection.cursor()
        # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")

    payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "payment.html", {'total_amount': total_amount})

def success(request):
    if 'user' in request.session:
        # Get the user from session
        s = sign_up.objects.get(username=request.session['user'])

        # Retrieve input data from session
        d = request.session['inputSymptoms']
        e = request.session['service_date']
        f = request.session['inputDoctorName']

        # Get the doctor from the database using the doctor's name
        t = add_doctor.objects.get(doctorname=f)

        # Create the appointment
        appointment = appointment1.objects.create(
            appointment_user_details=s,
            appointment_doctor_details=t,
            symptoms=d,
            appointment_date=e
        )

        # Pass the appointment details to the success template
        return render(request, 'success.html', {
            'user': s,
            'doctor': t,
            'symptoms': d,
            'appointment_date': e,
            'doctor_name': f
        })
    else:
        return redirect('login')  # Adjust the redirect if needed


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = sign_up.objects.get(email=email)
        except:  # noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)

            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})


