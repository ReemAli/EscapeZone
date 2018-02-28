from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/',views.profile, name='profile'),

    path('search', views.searchFunc, name='search'),
    #book
    path('books/', views.getAllBooks, name='AllBooks'),
    path('book/<int:book_id>', views.getOneBook, name='oneBook'),

    #author
    path('authors/', views.getAllAuthors, name='AllAuthors'),
    path('author/<int:author_id>', views.getOneAuthor, name='oneAuthor'),

    #catagory
    path('catagories/', views.getAllCats, name='AllCat'),
    path('catagory/<int:cat_id>', views.getOneCat, name='OneCat'),    

    path('login/', auth_views.login,{'template_name': 'escapeZone/login.html'} ,name='login'),
    path('logout/', auth_views.logout,{'template_name': 'escapeZone/home.html'} ,name='logout'),

    path('signup/', views.signup, name='signup'),
    
]