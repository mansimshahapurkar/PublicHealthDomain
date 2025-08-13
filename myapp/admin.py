from django.contrib import admin
from .models import Profile, Message, Feedback

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('timestamp',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at')
    search_fields = ('user__username', 'message')
    list_filter = ('submitted_at',)
