# Generated by Django 4.1 on 2024-03-02 04:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_remove_result_name_result_exam_alter_exam_exam_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="subject",
        ),
    ]