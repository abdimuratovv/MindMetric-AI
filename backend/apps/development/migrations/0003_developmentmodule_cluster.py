from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('development', '0002_developmentenrollment_completed_lesson_keys')]

    operations = [
        migrations.AddField(
            model_name='developmentmodule', name='cluster',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Academic'), (2, 'Algorithmic/practical')], default=1),
        ),
        migrations.AlterModelOptions(
            name='developmentmodule', options={'ordering': ['cluster', 'order', 'key', '-version']},
        ),
        migrations.AddConstraint(
            model_name='developmentmodule',
            constraint=models.CheckConstraint(check=models.Q(cluster__in=[1, 2]), name='dev_module_valid_cluster'),
        ),
    ]
