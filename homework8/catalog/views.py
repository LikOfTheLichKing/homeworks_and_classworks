from django.views import generic
from .models import Book, Author, BookInstance, Genre
from .forms import ReserveBookForm
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


class AuthorCreateView(generic.CreateView):
    model = Author
    fields = "__all__"


class AuthorUpdateView(generic.UpdateView):
    model = Author
    fields = "__all__"


class AuthorDeleteView(generic.DeleteView):
    model = Author
    fields = "__all__"
    success_url = "/catalog"


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    queryset = Book.objects.all()
    template_name = "book/list.html"


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    queryset = Author.objects.all()
    template_name = "author/list.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "author/detail.html"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book/detail.html"


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()

    return render(
        request,
        "index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_authors": num_authors,
        },
    )


def reserve_book_form(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = ReserveBookForm(request.POST)

        if form.is_valid():
            # Perform action
            book_instance.status = "r"
            book_instance.due_back = form.cleaned_data["return_date"]

            book_instance.save()

            # Redirect to success url
            return HttpResponseRedirect("/")
    else:
        proposed_return_date = datetime.date.today() + datetime.timedelta(
            weeks=3
            )
        form = ReserveBookForm(initial={"return_date": proposed_return_date})

    return render(
        request,
        "book/reserve.html",
        {"form": form, "book_instance": book_instance},
    )
