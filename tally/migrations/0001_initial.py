# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('pattern', models.CharField(default='*', max_length=100)),
                ('resolution', models.IntegerField(default=5, help_text='Resolution in seconds.')),
                ('retention', models.IntegerField(default=24, help_text='Retention period in hours.')),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                u'ordering': ('retention', 'resolution'),
            },
            bases=(models.Model,),
        ),
    ]
