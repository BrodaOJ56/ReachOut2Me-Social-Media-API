# Generated by Django 4.2 on 2023-04-13 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ReachOut2Me", "0002_userprofile_country_userprofile_date_of_birth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(null=True, upload_to="avatars/"),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="country",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="date_of_birth",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="state_or_city",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="telephone_number",
            field=models.CharField(max_length=20, null=True),
        ),
    ]