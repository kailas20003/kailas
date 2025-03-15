from django.db import models

# Create your models here.
class sign_up(models.Model):
    username=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.IntegerField()
    password=models.CharField(max_length=30)
    role = models.CharField(max_length=10, default='user', choices=[('user', 'User'), ('admin', 'Admin')])


class add_doctor(models.Model):
    doctorname=models.CharField(max_length=30)
    phoneno=models.IntegerField()
    department=models.CharField(max_length=40)
    image=models.ImageField()
    doctorusername=models.CharField(max_length=30)
    doctorpassword=models.CharField(max_length=30)
    role = models.CharField(max_length=10,default='doctor')


class add_treatment(models.Model):
    treatmentname = models.CharField(max_length=30)
    about = models.CharField(max_length=300)
    logo = models.ImageField()

class contact1  (models.Model):
    user_details=models.ForeignKey(sign_up,on_delete=models.CASCADE)
    message = models.CharField(max_length=300)


from django.db import models

class appointment1(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    appointment_user_details = models.ForeignKey(sign_up, on_delete=models.CASCADE)
    appointment_doctor_details = models.ForeignKey(add_doctor, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=50)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20, blank=True, null=True)  # Store time slot here
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment with {self.appointment_user_details.username} on {self.appointment_date}"
class PasswordReset(models.Model):
    user_details = models.ForeignKey(sign_up,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)

