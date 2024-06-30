from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


# menu = [
#     {'title': 'О сайте', 'url_name': 'about'},
#     {'title': 'Добавить статью', 'url_name': 'add_page'},
#     {'title': 'Обратная связь', 'url_name': 'contact'},
#     {'title': 'Войти', 'url_name': 'login'},
# ]

class Myclass:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Create your views here.
# def index(request): #HttpRequest
#     # t= render_to_string('women/index.html')
#     # return HttpResponse(t)
#     post = Women.published.all().select_related('cat')
#
#     data = {'title': 'Главная страница',
#             'menu': menu,
#             # 'float': 56.56,
#             # 'lst': [1, 2, 'abc', True],
#             # 'set': {1, 2, 3, 4, 5},
#             # 'dict': {'key_1':'value_1', 'key_2': 'value_2'},
#             # 'obj': Myclass(10, 20),
#             # 'url': slugify("The Main Page"),
#             'posts': post,
#             'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)

class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'cat_selected': 0,
    # }

    def get_queryset(self):
        return Women.published.all().select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] =  Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(f):
#     with open(f'uploads/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

@login_required  #(login_url='/admin/')
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         #handle_uploaded_file(form.cleaned_data['file'])
    #         fp = UploadFiles(file=form.cleaned_data['file'])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


# def categories(request, cat_id):
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")
#
#
# def categories_by_slug(request, cat_slug):
#     if request.POST:
#         print(request.POST)
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")
#
# def archive(request, year):
#     if year > 2024:
#         uri = reverse('cats_slug', args=('sport',))
#         return HttpResponsePermanentRedirect(uri)
#
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>{year}</p>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     data ={
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'women/post.html', data)

class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    #model = Women
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    #model = Women
    #fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags'] #'__all__'
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women' # <приложение>.<действие>_<таблица>

    # extra_context = {
    #     'menu': menu,
    #     'title': 'Добавление статьи'
    # }

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']  #'__all__'
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Редактирование статьи'
    # }


class DeletePage(DataMixin, DeleteView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']  #'__all__'
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Удаление статьи статьи'
    # }


# class AddPage(FormView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи'
#     }
#     def form_valid(self, form):
#         form.save()
#         return super.for_valid(form)


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#
#         #form.fields['is_published']=True
#         if form.is_valid():
#             #print(form.cleaned_data)
#
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             #Women.objects.filter(pk=Women.objects.latest('pk').pk).update(is_published=True)
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'women/addpage.html', data)

# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)

@permission_required(perm='women.add_women', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {'title': f'Рубрика:{category.name}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        # context['title'] = 'Категория - ' + cat.name
        # context['menu'] = menu
        # context['cat_selected'] = cat.pk
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selectred=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.women.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)

class TagsPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        # context['title'] = 'Тег: ' + tag.tag
        # context['menu'] = menu
        # context['cat_selected'] = None
        return self.get_mixin_context(context, title='Тег: ' + tag.tag, )
