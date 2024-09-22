# face_detection/admin.py
from django.contrib import admin
from .models import FaceSignIn

@admin.register(FaceSignIn)
class FaceSignInAdmin(admin.ModelAdmin):
    list_display = ('username',)  # Display the username in the admin list view
