from django.db import models

class FaceSignIn(models.Model):
    username = models.CharField(max_length=255, unique=True)
    photo = models.BinaryField()

    def __str__(self):
        return self.username
