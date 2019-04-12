from django.db import models

# Create your models here.
class Movie(models.Model):

    name = models.CharField(max_length=100, verbose_name="电影名称")
    score = models.CharField(max_length=100, verbose_name="电影评分")
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "电影"