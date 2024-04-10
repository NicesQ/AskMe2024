from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

import random
from faker import Faker
from faker.providers import person

from app.models import Question, Answer, Tag, Profile, Like


USER_COUNT = 1
TAGS_COUNT = 1
QUESTIONS_COUNT = 10
ANSWERS_COUNT = 100
VOTES_COUNT = 200


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()
        self.faker.add_provider(person)


    def add_arguments(self, parser):
        parser.add_argument('--ratio')


    def create_users(self, count : int):
        users = [User
            (
                username = self.faker.unique.user_name(),
                email = self.faker.unique.email(),
                password = self.faker.password()
            )  for i in range(count)
        ]
        User.objects.bulk_create(users)


    def create_profiles(self, count : int):
        user = User.objects.all()
        profiles = [Profile
                (
                    avatar = f'/static/img/test-avatar-{random.randint(1, 8)}.jpg',
                    nickname = self.faker.first_name(),
                    owner = user[i],
                ) for i in range(count)
            ]
        Profile.objects.bulk_create(profiles)


    def create_tags(self, count : int):
        tags = [Tag(value = self.faker.word()) for i in range(count)]
        Tag.objects.bulk_create(tags)


    def create_questions(self, count : int):
        profiles = Profile.objects.all()
        questions = [Question
                (
                    title = self.faker.paragraph(1)[:-1] + '?',
                    text = self.faker.paragraph(random.randint(5, 10)),
                    author = random.choice(profiles),
                ) for i in range(count)
            ]
        questions = Question.objects.bulk_create(questions)
        tags = []
        for i in range(count):
            tags_count = random.randint(1, 6)
            for j in range(tags_count):
                questions[i].tags.add(random.choice(Tag.objects.all()))

    def create_answers(self, count : int):
        questions = Question.objects.all()
        profiles = Profile.objects.all()
        answers = [Answer
            (
                title = self.faker.paragraph(1)[:-1] + '?',
                text = self.faker.paragraph(random.randint(4, 10)),
                question = random.choice(questions),
                author = random.choice(profiles),
            ) for i in range(count)
        ]
        Answer.objects.bulk_create(answers)


    def create_questions_likes(self, count : int):
        profiles = Profile.objects.all()
        questions_ids = Question.objects.values_list('id', flat=True)
        questions_type = ContentType.objects.get_for_model(Question)
        questions_likes = [Like(content_type = questions_type, value = 1, owner = random.choice(profiles), object_id = random.choice(questions_ids)) for i in range(count)]
        Like.objects.bulk_create(questions_likes)


    def create_answers_likes(self, count : int):
        profiles = Profile.objects.all()
        answers_ids = Answer.objects.values_list('id', flat=True)
        answers_type = ContentType.objects.get_for_model(Answer)
        answers_likes = [Like(content_type = answers_type, value = 1, owner = random.choice(profiles), object_id = random.choice(answers_ids)) for i in range(count)]
        Like.objects.bulk_create(answers_likes)


    def create_technical_likes_for_questions(self):
        questions = Question.objects.all()
        for question in questions:
            Like.objects.create(content_type = ContentType.objects.get_for_model(Question), value = 0, owner = question.author, object_id = question.id)
    
    
    def create_technical_likes_for_answers(self):
        answers = Answer.objects.all()
        for answer in answers:
            Like.objects.create(content_type = ContentType.objects.get_for_model(Answer), value = 0, owner = answer.author, object_id = answer.id)        
        
        
    def handle(self, *args, **options):
        ratio = None
        if options['ratio']:
            ratio = int(options['ratio'])
        else:
            ratio = 10000

        self.create_users(ratio * USER_COUNT)
        self.create_profiles(ratio * USER_COUNT)
        self.create_tags(ratio * TAGS_COUNT)
        self.create_questions(ratio * QUESTIONS_COUNT)
        self.create_answers(ratio * ANSWERS_COUNT)
        self.create_questions_likes(int(ratio * VOTES_COUNT / 2))
        self.create_answers_likes(int(ratio * VOTES_COUNT / 2))
        self.create_technical_likes_for_questions()
        self.create_technical_likes_for_answers()