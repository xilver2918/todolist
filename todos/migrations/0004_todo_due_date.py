# Generated for TODOLIST due date support.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_alter_todo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]