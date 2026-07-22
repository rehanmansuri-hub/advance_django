# Generated manually for Student module

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ors', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    CREATE TABLE IF NOT EXISTS sos_student (
                        id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        first_name varchar(50) NOT NULL,
                        last_name varchar(50) NOT NULL,
                        email varchar(100) NOT NULL,
                        mobile_no varchar(20) NOT NULL,
                        dob date NOT NULL,
                        gender varchar(50) NOT NULL,
                        college_id integer NOT NULL,
                        college_name varchar(50) NOT NULL
                    )
                    """,
                    reverse_sql="DROP TABLE IF EXISTS sos_student",
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name='Student',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('first_name', models.CharField(max_length=50)),
                        ('last_name', models.CharField(max_length=50)),
                        ('email', models.CharField(max_length=100)),
                        ('mobile_no', models.CharField(max_length=20)),
                        ('dob', models.DateField(max_length=20)),
                        ('gender', models.CharField(default='', max_length=50)),
                        ('college_id', models.IntegerField()),
                        ('college_name', models.CharField(max_length=50)),
                    ],
                    options={
                        'db_table': 'sos_student',
                    },
                ),
            ],
        ),
    ]