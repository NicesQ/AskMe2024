from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum, Count


class TagManager(models.Manager):
    def popular_tags(self):
        return self.annotate(rating = Count('questions')).order_by('-rating')[:10]
    
    
class Tag(models.Model):
    value = models.CharField(max_length=25, null=False)
    
    objects = TagManager()

    def __str__(self):
        return self.value


class QuestionManager(models.Manager):
    def top(self):
        return self.annotate(rating = Sum('upvotes__value')).order_by('-rating')

    def new(self):
        return self.order_by('-pub_date')

    def tag(self, tag_id):
        tag = Tag.objects.get(id = tag_id)
        return tag.questions.annotate(rating = Sum('upvotes__value')).order_by('-rating')
    
    
class Question(models.Model):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    upvotes = GenericRelation('Like', related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    author = models.ForeignKey('Profile', on_delete=models.RESTRICT, related_name='questions')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    def get_tags(self):
        return self.tags.all()

    def get_text(self):
        return (self.text[:140] + '...') if len(self.text) > 160 else self.text

    def get_answers(self):
        return self.answers.all()

    def get_likes(self):
        return self.upvotes.sum_likes()


class AnswerManager(models.Manager):
    def ordered_answers(self, quest_id):
        return self.filter(question_id = quest_id).annotate(rating = Sum('upvotes__value')).order_by('-isCorrect').order_by('-rating')
    
    
class Answer(models.Model):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(null=False)
    isCorrect = models.BooleanField(default=False)
    upvotes = GenericRelation('Like', related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.RESTRICT, related_name='answers')
    author = models.ForeignKey('Profile', on_delete=models.RESTRICT, related_name='answers')
    pub_date = models.DateTimeField(auto_now_add=True)
    
    objects = AnswerManager()

    def __str__(self):
        return self.title

    def get_text(self):
        return  self.text
    
    def get_likes(self):
        return self.upvotes.sum_likes()

class ProfileManager(models.Manager):
    def top_profiles(self):
        return self.annotate(raiting = Count('questions')).order_by('-raiting')[:10]
    
    
class Profile(models.Model):
    avatar = models.ImageField(null=True, blank = True, default='/static/img/default-avatar-icon.jpg', upload_to='avatar/%Y/%m/%d/')
    nickname = models.CharField(max_length=25)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    
    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class LikeManager(models.Manager):
    use_for_related_fields = True

    def sum_likes(self):
        res = self.get_queryset().aggregate(Sum('value')).get('value__sum')
        if not res:
            res = 0
        return res
    

class Like(models.Model):
    value = models.PositiveIntegerField(default=1)
    owner = models.ForeignKey(Profile,on_delete=models.RESTRICT, related_name='likes')
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    objects = LikeManager()

