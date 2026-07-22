from django.db import migrations


def repair_student_table(apps, schema_editor):
    Student = apps.get_model('ors', 'Student')
    table_name = Student._meta.db_table

    existing_tables = schema_editor.connection.introspection.table_names()
    if table_name not in existing_tables:
        schema_editor.create_model(Student)
        return

    table_description = schema_editor.connection.introspection.get_table_description(
        schema_editor.connection.cursor(),
        table_name,
    )
    existing_columns = {column.name for column in table_description}

    for field in Student._meta.local_fields:
        column_name = field.column
        if column_name not in existing_columns:
            schema_editor.add_field(Student, field)


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('ors', '0002_student'),
    ]

    operations = [
        migrations.RunPython(repair_student_table, migrations.RunPython.noop),
    ]