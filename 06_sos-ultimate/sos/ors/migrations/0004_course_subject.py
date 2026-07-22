# Generated manually for Course module

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ors', '0003_repair_student_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'sos_course',
            },
        ),
    ]
