from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import Blog, Category, Popular
from .forms import BlogForm

from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import numpy as np
import japanize_matplotlib


class IndexView(ListView):
    template_name = "blogs/index.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        """ブログ記事が公開且つIDの古い順にデータを取得"""
        queryset = Blog.objects.filter(is_publick=True).order_by('-id')
        return queryset

    def get_context_data(self):
        """テンプレートへ渡すPopularインスタンスの作成"""
        context = super().get_context_data()
        context["populars"] = Popular.objects.all()
        return context

# def index(request):
#     """
#     Blogアプリトップページ
#     """
#     blogs = Blog.objects.filter(is_publick=True).order_by('-id')
#     paginator = Paginator(blogs, 10)
#     page = request.GET.get('page')
#     blogs_page = paginator.get_page(page)
#     populars = Popular.objects.all()
#     context = {
#             'blogs': blogs,
#             'blogs_page': blogs_page,
#             'populars': populars,
#     }
#     return render(request, 'blogs/index.html', context)


@login_required
def private_index(request):
    """
    非公開Blogリスト
    """
    private_blog = Blog.objects.filter(is_publick=False).order_by('-id')
    return render(request, 'blogs/private_index.html', {'private_blog': private_blog})


def detail(request, blog_id):
    """
    Blog詳細ページ
    ７月２９日：詳細ページの新着記事数を5記事に修正。
    """
    blog_new = Blog.objects.filter(is_publick=True).order_by('-id')[:5]
    blog = get_object_or_404(Blog, id=blog_id, is_publick=True)
    context = {
            'blog': blog,
            'blog_new': blog_new
    }
    return render(request, 'blogs/detail.html', context)


@login_required
def private_detail(request, pk):
    """
    非公開Blogの詳細
    """
    private_detail = get_object_or_404(Blog, id=pk, is_publick=False)
    return render(request, 'blogs/private_detail.html', {'private_detail': private_detail})


@login_required
def new_blog(request):
    """
    Blog作成フォーム
    """
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "投稿が完了しました。")
            return redirect('blogs:index')
    else:
        form = BlogForm
    return render(request, 'blogs/new_blog.html', {'form': form })


@login_required
def edit_blog(request, blog_id):
    """
    Blog更新フォーム
    """
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "編集完了しました。")
            return redirect('blogs:index')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/edit_blog.html', {'form': form, 'blog': blog })


class CategoryView(ListView):
    template_name = "blogs/index.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        """カテゴリー別でブログ記事が公開且つIDの古い順にデータを取得"""
        # 404エラーを使用した方法
        # category = get_object_or_404(Category, title=self.kwargs['category'])
        # queryset = Blog.objects.filter(is_publick=True, category=category).order_by('-id')
        
        # 404エラーを使わない方法
        category = self.kwargs['category']
        queryset = Blog.objects.filter(is_publick=True, category__title=category).order_by('-id')
        
        messages.success(self.request, 'カテゴリ：{}'.format(category))
        return queryset

    def get_context_data(self):
        """テンプレートへ渡すPopularインスタンスの作成"""
        context = super().get_context_data()
        context["populars"] = Popular.objects.all()
        return context

# def blogs_category(request, category):
#     """
#     Blogカテゴリー機能
#     """
#     category = get_object_or_404(Category, title=category)
#     #category = Category.objects.get(title=category)
#     blogs = Blog.objects.filter(category=category, is_publick=True).order_by('-id')
#     paginator = Paginator(blogs, 10)
#     page = request.GET.get('page')
#     blogs_page = paginator.get_page(page)
#     populars = Popular.objects.all()
#     context = {
#             'blogs': blogs,
#             'category': category,
#             'blogs_page': blogs_page,
#             'populars': populars,
#     }
#     return render(request, 'blogs/index.html', context)


@login_required
def release(request, pk):
    """
    Blog公開用
    """
    blog_release = get_object_or_404(Blog, id=pk, is_publick=False)
    blog_release.to_release()
    return redirect('blogs:private_index')


@login_required
def private(request, pk):
    """
    Blog非公開用
    """
    blog_private = get_object_or_404(Blog, id=pk, is_publick=True)
    blog_private.to_private()
    return redirect('blogs:index')


def category_graph(request):
    """
    Blogカテゴリーのグラフ

    """
    plt.rcParams.update({'figure.autolayout': True})
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.patch.set_facecolor('whitesmoke')#背景の指定

    """ここにデータを作成する"""
    category_choice = Category.objects.all()
    blogs_choice = Blog.objects.select_related('category').all()

    x1 = [data.title for data in category_choice]
    y1 = [data.category_id for data in blogs_choice]
    y1 = np.unique(y1, return_counts=True)

    colorlist = ['r', 'y', 'g', 'b', 'm', 'c', '#ffff33', '#f781bf']
    ax.bar(x1, y1[1], color=colorlist, width=0.3, alpha=0.5)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    fig.clear()
    response['Content-Length'] = str(len(response.content))
    return response
