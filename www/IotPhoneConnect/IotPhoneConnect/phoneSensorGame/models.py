from django.db import models


class UserInfo(models.Model):
	name=models.CharField(max_length=20)
	uuid=models.CharField(max_length=50)
	createTime=models.DateTimeField()
	score=models.IntegerField()
	#class Meta:
	#	ordering = ['-score',]
	def __unicode__(self):
		return self.uuid
# Create your models here.
