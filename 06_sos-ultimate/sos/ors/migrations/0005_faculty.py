# Generated manually for Faculty module

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ors', '0004_course_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('qualification', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=20)),
                ('college_id', models.IntegerField()),
                ('college_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'sos_faculty',
            },
        ),
    ]
