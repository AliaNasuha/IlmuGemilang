# Generated by Django 4.2.4 on 2024-06-18 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ilmugemilang', '0004_class_alter_teacher_studclass_delete_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ilmugemilang.class')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ilmugemilang.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ilmugemilang.subject')),
            ],
        ),
    ]