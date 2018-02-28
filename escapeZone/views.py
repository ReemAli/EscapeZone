from django.shortcuts import render
from .models import Book
from .models import Author
from .models import Catagory
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm

# # home page
def home(request):
	if request.user.is_authenticated:
		top10Authors = Author.objects.all().order_by('-followers')[:10]
		top10Books = Book.objects.all().order_by('-rate')[:10]
		 # 'notify' : notifyBooks
		return render(request,'escapeZone/home.html', { 'books10':top10Books , 'authors10':top10Authors})
# 		# topRated = Book.objects.raw('select escapeZone_userrateperbook.book_id,escapeZone_book.id, avg(rate) as rate from escapeZone_userrateperbook , escapeZone_book where escapeZone_userrateperbook.book_id = escapeZone_book.id group by book_id order by rate desc limit 3')
# 		mostFollowed = Author.objects.raw('select escapeZone_author_follow.author_id,escapeZone_author.id, count(escapeZone_author_follow.author_id) as followers from escapeZone_author_follow, escapeZone_author where escapeZone_author.id = escapeZone_author_follow.author_id group by author_id order by followers desc limit 3')
# 		books= Book.objects.all()
# 		authors= Author.objects.all()
# 		cats= Catagory.objects.all()
# 		return render(request, 'escapeZone/home.html', { 'mostFollowed' : mostFollowed, 'books' : books, 'cats' : cats, 'authors' : authors })
	else:
		return redirect('login')


# #book
def getOneBook(request, book_id):
	bookObj = get_object_or_404(Book,id=book_id)
	if request.method == 'POST':	
		if request.POST.get('request')=='Read':
			try:
				bookObj.read.get(id=request.user.id)
				bookObj.read.remove(request.user.id)
			except Exception as ex:
				bookObj.read.add(request.user.id)
				bookObj.wish.remove(request.user)
			#wish
		elif request.POST.get('request')=='wishlist':
			try:
				bookObj.wish.get(id=request.user.id)
				bookObj.wish.remove(request.user.id)
			except Exception as ex:
				bookObj.wish.add(request.user)
				sbookObj.read.remove(request.user)
			bookObj.save()
		elif request.POST.get('request')=='vote':
			vstar = request.POST.get('star')
			UserRatePerBook.objects.create(rate=vstar , user=request.user.id , book= book_id)
			avgbookrate=UserRatePerBook.objects.all().aggregate(Avg('rate'))
			print(avgbookrate)
			print(avgbookrate.rate)
			avgbookrate = avgbookrate.__ceil__()
			if avgbookrate > 5:
				avgbookrate =5
			print(avgbookrate)
			Book.objects.filter(id=book_id).update(rate=avgbookrate)			
		return  redirect('/escapeZone/book/'+str(book_id))
		#get request 
	else :
		read = False
		wishlist= False
		try:
			bookObj.read.get(id=request.user.id)
		except Exception as ex:
			read=True
		try:
			bookObj.wishlist.get(id=request.user.id)
		except Exception as ex:
			wishlist=True
		return render(request,'escapeZone/book.html', {'book': bookObj,'read':read,'wishlist':wishlist})
# 	bookObj = get_object_or_404(Book, pk=book_id)
# 		#post request 
# 	if request.method == 'POST':
		
# 		if request.POST.get('request')=='read':
# 			bookObj.read.add(request.user)
# 			bookObj.wish.remove(request.user)
# 		#wish
# 		else :
# 			bookObj.wish.add(request.user)
# 			bookObj.read.remove(request.user)
# 		bookObj.save()
# 		return redirect('/escapeZone/book/'+str(book_id))
# 	# #get request 
# 	else :
# 		read= False
# 		wish = False
# 		try:
# 			bookObj.read.get(id =0 request.user.id)
# 		except Exception as e:
# 			read = True

# 		try: 
# 			bookObj.wish.get(id = request.user.id)
# 		except Exception as e:
# 			wish = True	
# 		# book.read.get(id=request.user.id).id
# 		# book.wish.get(id=request.user.id).id 
# 		return render(request, 'escapeZone/book.html',{'book': bookObj, 'read':read ,'wish':wish})
 
def getAllBooks(request):
	# books= Book.objects.all()
	
	if request.method == 'POST':
		bookid =  request.POST.get('bk_id')
		bookObj = get_object_or_404(Book,id=bookid)	
		
		if request.POST.get('request')=='Read':
			try:
				bookObj.read.get(id=request.user.id)
				bookObj.read.remove(request.user.id)
			except Exception as ex:
				bookObj.read.add(request.user.id)
				bookObj.wish.remove(request.user)
		else:
			try:
				bookObj.wish.get(id=request.user.id)
				bookObj.wish.remove(request.user.id)
				print("rmw")

			except Exception as ex:
				bookObj.wishlist.add(request.user)
				bookObj.read.remove(request.user)
		bookObj.save()

	books= Book.objects.all()
	return render(request, 'escapeZone/books.html',{'books':books})
# #author
def getOneAuthor(request, author_id):
	authorObj = get_object_or_404(Author,pk=author_id)
	if request.method == 'GET':
		follow = False
		try:
			authorObj.follow.objects.get(id= request.user.id)
		except Exception as ex:
			follow= True
		return render(request, 'escapeZone/author.html',{'author': authorObj, 'follow':follow})

	if request.method == 'POST':
		if request.POST.get('request')=='follow' :
			try:
				authorObj.follow.get(id=request.user.id)
				authorObj.follow.remove(request.user.id)
				authorObj.followers =authorObj.followers - 1
				# Author.objects.filter(author_name = authorObj.author_name).update(followers = followers - 1)

			except Exception as ex:
				authorObj.follow.add(request.user)
				authorObj.followers =authorObj.followers + 1
				# Author.objects.filter(author_name = authorObj.author_name).update(followers = followers + 1)

		authorObj.save()
		return redirect('/escapeZone/author/'+str(author_id))
# 	authorObj = get_object_or_404(Author, pk=author_id)
	
# 	if request.method == 'POST':
		
# 		if request.POST.get('request')=='follow':
# 			authorObj.follow.add(request.user)
# 		#
# 		else :
# 			authorObj.unfollow.remove(request.user)
# 		authorObj.save()
# 		return redirect('/escapeZone/author/'+str(author_id))
# 	else :
# 		follow= False
# 		try:
# 			authorObj.follow.get(id = request.user.id)
# 		except Exception as e:
# 			follow = True

# 		return render(request, 'escapeZone/author.html',{'author': authorObj, 'follow':follow})

def getAllAuthors(request):
	if request.method == 'POST':
		authid = request.POST.get('auth_id')
		authorObj = get_object_or_404(Author,pk=authid)
		if request.POST.get('request')=='follow' :
			try:
				authorObj.follow.get(id=request.user.id)
				authorObj.follow.remove(request.user.id)
				authorObj.followers =authorObj.followers - 1
				# Author.objects.filter(author_name = authorObj.author_name).update(followers = followers - 1)

			except Exception as ex:
				authorObj.follow.add(request.user)
				authorObj.followers =authorObj.followers + 1
				# Author.objects.filter(author_name = authorObj.author_name).update(followers = followers + 1)

		authorObj.save()	
	authors= Author.objects.all()
	return render(request, 'escapeZone/authors.html',{'authors':authors})



# #catagory
def getOneCat(request, cat_id):
	catObj = get_object_or_404(Catagory, pk=cat_id)
	if request.method == 'GET':
		favorite=False
		try:
			catObj.objects.get(id = request.user.id)
		except Exception as ex:
			favorite =True
		return render(request, 'escapeZone/catagory.html',{'catObj': catObj, 'favorite':favorite})
	if request.method == 'POST':
		if request.POST.get('request')==' favorite':
			try:
				catObj.objects.get(id = request.user.id)
				catObj.favorite_Category.remove(request.user)
			except Exception as ex:
				catObj.favorite_Category.add(request.user)
		catObj.save()
		return redirect('/escapeZone/catagory/'+str(cat_id))

def getAllCats(request):	
	if request.method == 'POST':
		cid = request.POST.get('cat_id')
		catObj = get_object_or_404(Catagory, pk=cid)
		if request.POST.get('request')==' favorite':
			try:
				catObj.objects.get(id = request.user.id)
				catObj.favorite_Category.remove(request.user)
			except Exception as ex:
				catObj.favorite_Category.add(request.user)
		catObj.save()

	cats= Catagory.objects.all()
	return render(request, 'escapeZone/catagories.html',{'cats':cats})


def signup(request):
	msg = []
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			row_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=row_password)
			login(request, user)
			return redirect('home')
	else:
		msg.append("invalid Data")
		form = UserCreationForm()
	return render(request, 'escapeZone/signup.html', {'form': form})


#search function
def searchFunc(request):

	se = request.GET.get('s')
	authors=Author.objects.filter(author_name__icontains=se)

	return render(request, 'escapeZone/authors.html',{'authors': authors})	
	

def profile(request):

	username = request.user.username
	id = request.user.id
	date_joined = request.user.date_joined
	readBk = Book.objects.filter(read=request.user.id)
	wishBk = Book.objects.filter(wish=request.user.id)
	favCat = Catagory.objects.filter(favorite_Category=request.user.id)
	follAuth = Author.objects.filter(follow=request.user.id)

	return render(request, 'escapeZone/profile.html',{'username': username, 'id': id, 'date_joined':date_joined , 'r':readBk ,'w':wishBk ,'f':favCat ,'fa':follAuth })

def editProfile(request):
	if request.method == 'POST':
		form = Edit(request.POST, use=request.user)
		if form.is_valid():
			form.save()
			return render(request, 'escapeZone/home.html')
	else:
		form=Edit(use=request.user)
		return render(request, 'escapeZone/edit.html',{'form':form})

def changePasswrd(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('updateUserPassword')
	else:
		form = PasswordChangeForm(user=request.user) 
		return render(request, 'escapeZone/changePasswrd.html', {'form': form})