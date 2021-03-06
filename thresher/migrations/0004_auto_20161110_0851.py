# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thresher', '0003_auto_20161021_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlehighlight',
            name='highlight',
        ),
        migrations.RemoveField(
            model_name='articlehighlight',
            name='topic',
        ),
        migrations.AddField(
            model_name='articlehighlight',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='article_highlights', to='thresher.UserProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articlehighlight',
            name='highlight_source',
            field=models.CharField(choices=[(b'HLTR', b'Highlighter'), (b'QUIZ', b'Quiz')], default='', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='highlightgroup',
            name='article_highlight',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='highlights', to='thresher.ArticleHighlight'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='highlightgroup',
            name='case_number',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='highlightgroup',
            name='highlight_text',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='highlightgroup',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_highlights', to='thresher.Topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[(b'mc', b'Multiple Choice'), (b'dt', b'Date Time'), (b'tb', b'Textbox'), (b'cl', b'Checklist')], default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submittedanswer',
            name='highlight_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_answers', to='thresher.HighlightGroup'),
        ),
        migrations.AlterField(
            model_name='submittedanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_answers', to='thresher.Question'),
        ),
        migrations.AlterField(
            model_name='submittedanswer',
            name='user_submitted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_answers', to='thresher.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([('parent', 'name')]),
        ),
    ]
