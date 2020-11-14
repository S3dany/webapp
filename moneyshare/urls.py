from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.list_persons, name='list_persons'),
    path('listgroup/<str:mygroup>', views.list_users, name='list_users'),
    path('new', views.create_group, name='create_group'),
    # path('update/<int:user_id>/', views.update_persons, name='update_persons'),
    path('connect/<str:operation>/<int:user_id>/<str:mygroup>', views.add_to_group, name='add_to_group'),
    path('createbill/<str:mygroup>/', views.create_bill, name='create_bill'),
    path('editbill/<str:mybill>/', views.edit_bill, name='edit_bill'),
    path('register', views.register, name='register'),
    path('send/<int:id>', views.send_friend_request, name='send'),
    path('accept/<int:id>', views.accept_friend_request, name='accept'),
    path('cancel/<int:id>', views.cancel_friend_request, name='cancel'),
    path('delete/<int:id>', views.delete_friend_request, name='delete'),

]