

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('content', models.TextField(blank=True, verbose_name='содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/blog/', verbose_name='превью')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('is_public', models.BooleanField(default=True, verbose_name='публикация')),
                ('num_views', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
