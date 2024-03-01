# Generated by Django 4.1 on 2024-03-01 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("semester", models.PositiveIntegerField()),
                ("year", models.PositiveIntegerField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "class_id",
                    models.CharField(editable=False, max_length=10, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("section", models.CharField(max_length=10)),
                ("year_of_join", models.PositiveIntegerField()),
                ("year_of_exit", models.PositiveIntegerField()),
                (
                    "course_id",
                    models.CharField(editable=False, max_length=10, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(blank=True, max_length=100)),
                ("credit", models.PositiveIntegerField(blank=True)),
                (
                    "class_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.staff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TimeTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.CharField(max_length=20)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "class_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.subject"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("register_number", models.CharField(max_length=20, unique=True)),
                ("date_of_birth", models.DateField()),
                ("gender", models.CharField(max_length=20)),
                ("phone", models.CharField(max_length=20)),
                (
                    "class_attending",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.course"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.department",
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.staff"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Result",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("grade", models.CharField(max_length=10)),
                ("grade_points", models.PositiveIntegerField()),
                (
                    "class_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.student"
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.subject"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Holiday",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.CharField(blank=True, max_length=200)),
                (
                    "class_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="department",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.department"
            ),
        ),
        migrations.AddField(
            model_name="class",
            name="coordinator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.staff"
            ),
        ),
        migrations.AddField(
            model_name="class",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.course"
            ),
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                (
                    "class_related",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.class"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.course"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.department",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.student"
                    ),
                ),
            ],
        ),
    ]
