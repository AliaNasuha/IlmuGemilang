from django.db import models

# Create your models here.
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=250)

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    studname = models.CharField(max_length=250, primary_key=True)
    studic = models.CharField(max_length=20)
    studage = models.PositiveIntegerField(default=2)
    housenum = models.CharField(max_length=15)
    mobilenum = models.CharField(max_length=15) 
    parentsnum = models.CharField(max_length=15)
    houseaddress = models.CharField(max_length=250)
    email = models.CharField(max_length=100)
    currentschool = models.CharField(max_length=100)
    standard = models.CharField(max_length=15) 
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.studname

class Class(models.Model):
    studclass = models.CharField(max_length=30, primary_key=True)
    subject = models.CharField(max_length=100)
    teachername = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.studclass} - {self.subject}"

class Teacher(models.Model):
    date = models.DateField()
    studclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    studname = models.ForeignKey(Student, on_delete=models.CASCADE) 


class AssignClass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.studname} - {self.subject.name} - {self.class_assigned.studclass}"
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])  
    
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentstatus = models.CharField(max_length=15, default='Not Paid')
    payment_date = models.DateField(null=True, blank=True)
    reference_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.student.studname} - {self.item}'


 