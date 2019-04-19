from django.shortcuts import render
#import model classes 
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.all().count()  # The 'all()' is implied by default.
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0) #get visits count, default=0
    request.session['num_visits'] = num_visits + 1  #every time you sent request, num++
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context,
    )
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
class AuthorDetailView(generic.DetailView):
    model = Author
#class BookListView(generic.ListView):
#    model = Book
#    context_object_name = 'my_book_list'   # your own name for the list as a template variable
#    queryset = Book.objects.all()[:5] # Get 5 books containing the title war
#    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
class BookDetailView(generic.DetailView):
    model = Book

class LoanedBooksByAllListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    template_name='catalog/bookinstance_list_borrowed_all.html'
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """

    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk = pk) #pk>id for bookInstance
    if request.method == 'POST':#以該頁面(renew_book_form)傳過來的request判斷方法屬性()
        form = RenewBookForm(request.POST)  #
        if form.is_valid():     #表單完全正確的路徑,最後會返回到全借書列表
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:                   #表單請求為Get,給予default回饋
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    context = {
        'form' : form,
        'bookinst' : book_inst,
    }
    return render(request, 'catalog/book_renew_librarian.html',context)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors') #延遲版本的reverse,在執行成功後回到作者列表

class BookCreate(CreateView):
    model = Book
    fields = ['title','author','summary','isbn','genre','language']
    #initial = 

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books') #延遲版本的reverse,在執行成功後回到作者列表
