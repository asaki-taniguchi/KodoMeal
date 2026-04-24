from django.db import models

class Post(models.Model):
    store_id = models.IntegerField()
    content = models.TextField()
    rating = models.IntegerField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    