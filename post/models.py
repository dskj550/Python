from django.db import models
from user.models import User
# Create your models here.

class Post(models.Model):
    class Meta:
        db_table='post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,null=False)
    postdate = models.DateTimeField(null=False)
    author = models.ForeignKey(User)

    def __repr__(self):
        return "<Post {} {}>".format(self.id,self.title)

    __str__ = __repr__

class Content(models.Model):

    class Meta:
        db_table = 'content'

    post = models.OneToOneField(Post)
    content = models.TextField(null=False)

    def __repr__(self):
        return "<Content {} {} {}>".format(self.pk,self.post.id,self.content[:20])

    __str__ = __repr__

