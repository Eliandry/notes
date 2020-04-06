from django.db import models

class Note(models.Model):
    number=models.IntegerField()
    text=models.TextField()

    def __repr__(self):
        return f'<Note number: {self.number}'