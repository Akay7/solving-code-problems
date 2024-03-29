# Generated by Django 3.2.6 on 2021-08-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                ("reply", models.TextField(db_index=True)),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("correct", "Correct"),
                            ("wrong", "Wrong"),
                            ("evaluation", "Evaluation"),
                        ],
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
