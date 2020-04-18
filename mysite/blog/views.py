from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2) # three post on page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Jeśli zmienna page niejest liczbą całkowitą
        # Wówczas pobeirana jest pierwsza strona z wyników
        posts = paginator.page(1)
    except EmptyPage:
        #Jeśli zmienna page ma wartość wiekszą niż numer ostatniej strony
        #wyników, wtedy pobierana jest ostatnia strona wyników
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})




class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # pobranie posta na podstawie jego identyfikatora
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Formularz wysłany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # weryfikacja pól zakończona powodzeniem
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) zachęcia do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            massage = 'Przeczytaj post "{}| na stronie {}\n\n Komentarz dodany przez {}: {}'.format
            (post.title,post.url, cd['name'], cd['comments'])
            send_mail(subject,massage, 'admin@myblog.com', [cd['to']])
            # w .... więc mozna wysłać formularz
        else:
            form = EmailPostForm()
        return  render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent' : sent})