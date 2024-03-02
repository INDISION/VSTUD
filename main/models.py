from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.code

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=10)
    year_of_join = models.PositiveIntegerField()
    year_of_exit = models.PositiveIntegerField()
    course_id = models.CharField(max_length=10, unique=True, editable=False)
    def __str__(self):
        return self.course_id
    def save(self, *args, **kwargs):
        self.course_id = f"{self.department}{str(self.year_of_join)[-2:]}{self.section}"
        super(Course, self).save(*args, **kwargs)
    
class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    coordinator = models.ForeignKey(Staff, on_delete=models.CASCADE)
    class_id = models.CharField(max_length=10, unique=True, editable=False)
    def __str__(self):
        return self.class_id
    def save(self, *args, **kwargs):
        self.class_id = f"{self.course}{str(self.semester)}"
        super(Class, self).save(*args, **kwargs)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_attending = models.ForeignKey(Class, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    mentor = models.ForeignKey(Staff, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        self.user.username = f"{self.course}{self.register_number[-3:]}"
        super(User, self.user).save(*args, **kwargs)
        super(Student, self).save(*args, **kwargs)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, blank=True, null=True)
    credit = models.PositiveIntegerField(blank=True, null=True)
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.name}-{self.staff}"

class Result(models.Model):
    name = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    grade_points = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.student}-{self.subject}-{self.grade}"
class Holiday(models.Model):
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return f"{self.start_date}-{self.end_date}-{self.description}"
    
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.student}-{self.status}"
    
class TimeTable(models.Model):
    class_related = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.class_related}-{self.day}"
