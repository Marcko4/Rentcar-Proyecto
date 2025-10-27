from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rentals', '0004_fill_reservation_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]