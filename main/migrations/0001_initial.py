# Generated by Django 5.0.2 on 2024-03-26 15:26

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.PositiveIntegerField()),
                ('year', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('class_id', models.CharField(blank=True, max_length=10, unique=True)),
            ],
            options={
                'ordering': ['class_id'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=10)),
                ('year_of_join', models.PositiveIntegerField()),
                ('year_of_exit', models.PositiveIntegerField()),
                ('course_id', models.CharField(blank=True, max_length=10, unique=True)),
            ],
            options={
                'ordering': ['course_id'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
            ],
            options={
                'ordering': ['class_related'],
            },
        ),
        migrations.AddField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.department'),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('register_number', models.CharField(max_length=20, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
        migrations.AddField(
            model_name='class',
            name='coordinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_number', models.CharField(max_length=20, unique=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('transportation', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('class_attending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['register_number'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=100)),
                ('credit', models.PositiveIntegerField()),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.staff')),
            ],
            options={
                'ordering': ['code'],
                'unique_together': {('code', 'class_related')},
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('exam_id', models.CharField(blank=True, max_length=100, unique=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject')),
            ],
            options={
                'ordering': ['exam_id'],
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=200)),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
            ],
            options={
                'ordering': ['date', 'class_related'],
                'unique_together': {('class_related', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(blank=True, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('grade_points', models.PositiveIntegerField(blank=True, null=True)),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
            options={
                'ordering': ['student__register_number'],
                'unique_together': {('exam', 'class_related', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('present_status', models.BooleanField(default=False)),
                ('class_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.student')),
            ],
            options={
                'ordering': ['student__register_number'],
                'unique_together': {('date', 'class_related', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject')),
            ],
            options={
                'ordering': ['subject'],
                'unique_together': {('subject', 'file')},
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject')),
            ],
            options={
                'ordering': ['day', 'start_time'],
                'unique_together': {('subject', 'day', 'start_time')},
            },
        ),
    ]
