# Generated by Django 2.0.1 on 2018-01-29 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailFragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=128)),
                ('body', models.TextField(blank=True, default='')),
                ('language', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mail_fragments', to='geo.Language')),
            ],
        ),
        migrations.CreateModel(
            name='MailSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, default='')),
                ('language', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.Language')),
            ],
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=64)),
                ('subject', models.CharField(default='', max_length=256)),
                ('body', models.TextField(blank=True, default='')),
                ('signature_included', models.BooleanField(default=True)),
                ('language', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mail_templates', to='geo.Language')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mailtemplate',
            unique_together={('reference', 'language')},
        ),
        migrations.AlterUniqueTogether(
            name='mailfragment',
            unique_together={('reference', 'language')},
        ),
    ]
