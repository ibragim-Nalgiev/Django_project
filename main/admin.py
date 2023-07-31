from django.contrib import admin

from main.models import Mailing, Message, LogiMail, Blog


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'periodicity', 'mailing_status', 'is_active')
    search_fields = ('periodicity', 'is_active',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'context')
    search_fields = ('title',)


@admin.register(LogiMail)
class LogiMailAdmin(admin.ModelAdmin):
    list_display = ('date_last', 'status', 'server_answer', 'mailing')
    search_fields = ('date_last', 'status',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'date_create', 'is_public', 'num_views')
    search_fields = ('title', 'date_create', 'is_public')
