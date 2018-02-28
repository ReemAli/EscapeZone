from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):

	author_name = models.CharField(max_length=200)
	acountry = models.CharField(max_length=20,default=None,null=True,blank=True)
	bornAt = models.DateField()
	diedAt = models.DateField(default=None,null=True,blank=True)
	bio = models.TextField(null= True)
	# pic = models.ImageField(upload_to = "/static/static/images")
	followers = models.IntegerField(null=True)
	follow = models.ManyToManyField(User,default=None,null=True,blank=True)
	def __unicode__ (self):
		return self.author_name
	def __str__ (self):
		return self.author_name

class Book(models.Model):
	book_name = models.CharField(max_length=150)
	publishedAt = models.DateField()
	# pic = models.ImageField(upload_to = "/static/static/images")
	rate = models.FloatField(default=0,null= True)
	desc = models.TextField(null=False)
	book_author = models.ForeignKey('Author',on_delete=models.CASCADE)
	book_catagory = models.ManyToManyField('Catagory')
	read = models.ManyToManyField(User,related_name='read', default=None,null=True,blank=True)
	wish =  models.ManyToManyField(User,related_name='wish', default=None,null=True,blank=True)	
	def get_Author_id(self):
		return self.book_author
	def __unicode__ (self):
		return self.book_name
	def __str__ (self):
		return self.book_name

class Catagory(models.Model):	
	cat_name = models.CharField(max_length=150)
	desc = models.TextField()
	# cat_Books=models.ManyToManyField(Book,related_name='catbook')
	favorite_Category=models.ManyToManyField(User,related_name="fav",default=None,null=True,blank=True)
	def __unicode__ (self):
		return self.cat_name
	def __str__ (self):
		return self.cat_name
	
class UserRatePerBook(models.Model):
	rate = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book,related_name="user_book_rate",on_delete=models.CASCADE)


	