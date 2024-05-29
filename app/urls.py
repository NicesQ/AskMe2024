from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('question/<int:question_id>',views.question, name='question'),
    path('log_in/',views.log_in, name='log_in'),
    path('log_out/',views.log_out, name='log_out'),
    path('register/',views.register, name='register'),
    path('settings/',views.settings, name='settings'),
    path('new/',views.new_question, name='new_question'),
    path('tags/<int:tag_id>',views.questions_by_tag, name='questions_by_tag'),
    path('like_async/<int:object_id>/<int:object_type>',views.like_async, name='like_async'),
    path('question/correct_change/<int:answer_id>/<int:question_id>',views.correct_answer_async, name="correct_answer_change")
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
            