from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
]


# from django.contrib import admin
# from django.urls import path
# from chatbot import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.chat_view, name='chat'),
# ]

