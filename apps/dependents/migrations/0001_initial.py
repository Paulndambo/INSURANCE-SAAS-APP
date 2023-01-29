# Generated by Django 4.1.1 on 2023-01-29 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('policies', '0001_initial'),
        ('schemes', '0001_initial'),
        ('users', '0003_policyholderrelative'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuneralBeneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('passport_number', models.CharField(max_length=255, null=True)),
                ('id_number', models.CharField(max_length=255, null=True)),
                ('address', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(null=True)),
                ('guardian_or_trustee_first_name', models.CharField(max_length=255, null=True)),
                ('guardian_or_trustee_last_name', models.CharField(max_length=255, null=True)),
                ('guardian_or_trustee_phone_number', models.CharField(max_length=255, null=True)),
                ('guardian_or_trustee_date_of_birth', models.DateField(null=True)),
                ('membership', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.membership')),
                ('policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='policies.policy')),
                ('relative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.policyholderrelative')),
                ('schemegroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schemes.schemegroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
