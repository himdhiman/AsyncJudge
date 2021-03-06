# Generated by Django 3.1.5 on 2021-01-29 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('note', models.TextField(blank=True, null=True)),
                ('level', models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')], max_length=20)),
                ('accuracy', models.IntegerField()),
                ('totalSubmissions', models.IntegerField()),
                ('sampleTc', models.IntegerField()),
                ('totalTC', models.IntegerField()),
                ('createdAt', models.DateField()),
                ('memoryLimit', models.CharField(blank=True, max_length=20, null=True)),
                ('timeLimit', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('problemId', models.IntegerField()),
                ('language', models.CharField(choices=[('CP', 'CPP'), ('JV', 'JAVA'), ('P3', 'PYTHON 3'), ('P2', 'PYTHON 2'), ('JS', 'JAVASCRIPT')], max_length=2)),
                ('code', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Q', 'QUEUED'), ('R', 'RUNNING'), ('AC', 'ACCEPTED'), ('CE', 'COMPILATION ERROR'), ('WA', 'WRONG ANSWER'), ('RE', 'RUNTIME ERROR')], max_length=2)),
                ('error', models.TextField(blank=True)),
                ('inputGiven', models.TextField(blank=True)),
                ('outputGen', models.TextField(blank=True)),
                ('testCasesPassed', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UploadTC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testcases', models.FileField(blank=True, null=True, upload_to='tempTC/')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.problem')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(to='api.Tag'),
        ),
    ]
