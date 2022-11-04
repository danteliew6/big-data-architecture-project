from django.urls import path
from . import views

#URL config
urlpatterns =[
    path('hello/', views.say_hello),
    path('popularskillsets/',views.popular_skillsets_chart),
    path('popularskills/',views.popular_skills),
    path('jobtitle/',views.job_title_chart),
    path('popularlanguages/',views.popular_languages_chart),
    path('show_range/',views.show_range)
]
