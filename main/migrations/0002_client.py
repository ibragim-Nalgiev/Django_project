

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='фамилия')),
                ('comment', models.TextField(blank=True, max_length=255, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
