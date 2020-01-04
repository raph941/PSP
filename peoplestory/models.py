from django.db import models
from accounts.models import User, UserProfile

#story approval status
APPROVED = 'APPROVED'
NOT_APPROVED = 'NOT_APPROVED'
PENDING = 'PENDING'

APPROVAL_STATUS = [
    (APPROVED, 'approved'),
    (NOT_APPROVED, 'not_approved'),
    (PENDING, 'pending'),
]


class Stories(models.Model):
    full_name = models.CharField(max_length = 255, null=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    story_caption = models.CharField(max_length=255)
    story = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='story_images/', default='default.jpg')    
    comment_count = models.IntegerField(blank=True, default=0, verbose_name=('comment count'))

    def __str__(self):
        return f'story about : { self.full_name }'

    class Meta:
        ordering = ['-last_updated']


class Comment(models.Model):
    story = models.ForeignKey(Stories, on_delete = models.CASCADE, related_name="comments")
    comment_author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_content = models.CharField(max_length = 200,verbose_name = "comment")
    comment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'by : { self.comment_author }'

    class Meta:
        ordering = ['-comment_date']