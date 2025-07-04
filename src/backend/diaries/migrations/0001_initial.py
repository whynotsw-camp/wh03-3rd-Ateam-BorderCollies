# Generated by Django 4.2.20 on 2025-05-15 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("events", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Diary",
            fields=[
                ("diary_id", models.AutoField(primary_key=True, serialize=False)),
                ("diary_date", models.DateField(default=django.utils.timezone.now)),
                ("final_text", models.TextField()),
                ("timeline_sent", models.JSONField(blank=True, null=True)),
                ("markers", models.JSONField(blank=True, null=True)),
                ("camera_target", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "일기",
                "verbose_name_plural": "일기 목록",
            },
        ),
        migrations.CreateModel(
            name="Emotion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("emotion_label", models.CharField(max_length=50, unique=True)),
                ("emoji", models.CharField(default="😀", max_length=4)),
                ("order", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="DiaryKeyword",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_selected", models.BooleanField(default=True)),
                ("is_auto_generated", models.BooleanField(default=False)),
                (
                    "diary",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="diaries.diary"
                    ),
                ),
                (
                    "keyword",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.keyword"
                    ),
                ),
            ],
            options={
                "verbose_name": "일기 키워드",
                "verbose_name_plural": "일기 키워드 목록",
                "db_table": "diary_keyword",
                "unique_together": {("diary", "keyword")},
            },
        ),
        migrations.AddField(
            model_name="diary",
            name="keywords",
            field=models.ManyToManyField(
                related_name="diaries",
                through="diaries.DiaryKeyword",
                to="events.keyword",
            ),
        ),
        migrations.AddField(
            model_name="diary",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
