import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiry', models.DateTimeField(default='reservation.models.reservation.calculate_expiry')),
                ('confirmed', models.BooleanField(default=False)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.appointment')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.client')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.provider')),
            ],
        ),
    ]
