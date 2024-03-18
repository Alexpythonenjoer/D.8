from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
# Create your models here.
class Author(models.Model):
    author=models.OneToOneField(User, on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)

    def update_rating(self):
        post_rating=0
        comments_rating=0
        posts_comments_rating=0
        posts=Posts.objects.filter(author=self)
        for i in posts:
            post_rating+=i.rating
        comments=Comments.objects.filter(user=self.author)
        for c in comments:
            comments_rating+=c.rating
        posts_comments=Comments.objects.filter(post_connect__author=self)
        for p in posts_comments:
            posts_comments_rating+=p.raitng

        self.rating = post_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    category_name=models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.category_name


class Posts(models.Model, ):
    news='N'
    artickle='A'
    CHOOSE=[(artickle,'статья'),(news,'новость')]
    type=models.CharField(max_length=1,choices=CHOOSE,default=news)
    posts_author=models.ForeignKey(Author, on_delete=models.CASCADE)
    when=models.DateField(auto_now_add=True)
    category_postcat=models.ManyToManyField(Category, through='PostCategory',related_name='posts')
    title=models.CharField(max_length=255, unique=True, validators=[MinValueValidator(0)])
    text_of_posts= models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('posts_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}:{self.text_of_posts}'

    def preview(self):
        return self.text_of_posts[0:124]+'...'

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()


class PostCategory(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    categories=models.ForeignKey(Category, on_delete=models.CASCADE)

class Comments(models.Model):
    post_connect=models.ForeignKey(Posts,on_delete=models.CASCADE)
    user_conkat=models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text=models.TextField()
    comment_make_time=models.DateField(auto_now_add=True)
    comment_rating=models.FloatField(default=0.0)

    def like(self):
        self.comment_rating+=1
        self.save()

    def dislike(self):
        self.comment_rating-=1
        self.save()



