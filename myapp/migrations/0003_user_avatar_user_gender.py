# Generated by Django 4.2.13 on 2024-10-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_rename_user_id_image_user_remove_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                default="images/avatars/man_default.jpg", upload_to="images/avatars"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.IntegerField(choices=[(1, "男"), (2, "女")], default=1),
        ),
    ]
