import io

import japanize_matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from django.contrib import messages  # type: ignore
from django.http import HttpResponse  # type: ignore
from django.shortcuts import get_object_or_404, redirect  # type: ignore
from django.urls import reverse_lazy  # type:ignore
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View  # type: ignore
from matplotlib.backends.backend_agg import FigureCanvasAgg  # type: ignore

from .forms import BlogForm
from .models import Blog, Category


class IndexView(ListView):
    template_name = "blogs/index.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        """ブログ記事が公開且つIDの古い順にデータを取得"""
        queryset = Blog.objects.filter(is_publick=True).order_by("-id")
        return queryset


class CategoryView(ListView):
    template_name = "blogs/index.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        """カテゴリー別でブログ記事が公開且つIDの古い順にデータを取得"""
        # 404エラーを使用した方法
        category = get_object_or_404(Category, title=self.kwargs["category"])
        queryset = Blog.objects.filter(is_publick=True, category=category).order_by("-id")
        messages.success(self.request, f"カテゴリ:{category}")
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = "blogs/detail.html"
    context_object_name = "blog"

    def get_context_data(self, **kwargs):
        """テンプレートへ渡す新着記事のインスタンスの作成"""
        context = super().get_context_data(**kwargs)
        context["new_articls"] = self.model.objects.filter(is_publick=True).order_by(
            "-id"
        )[:5]
        return context


class PrivateIndexView(ListView):
    queryset = Blog.objects.filter(is_publick=False).order_by("-id")
    template_name = "blogs/private_index.html"
    context_object_name = "private_blog"

    def get(self, request):
        """管理人以外のアクセスはHTMLページでコメントを返す"""
        if not request.user.is_authenticated:
            return HttpResponse("<h1>権限がありません。</h1>")
        return super().get(request)


class PrivateDetailView(DetailView):
    model = Blog
    template_name = "blogs/private_detail.html"
    # context_object_name = 'private_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["private_detail"] = get_object_or_404(
            Blog, id=self.kwargs["pk"], is_publick=False
        )
        return context

    def get(self, request, pk):
        """管理人以外のアクセスはHTMLページでコメントを返す"""
        if not request.user.is_authenticated:
            return HttpResponse("<h1>権限がありません。</h1>")
        return super().get(request, pk)


class BlogFormView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/new_blog.html"
    success_url = reverse_lazy("blogs:index")
    get_object_name = "blog"

    def form_valid(self, form):
        """検証が終わったらメッセージを表示する"""
        messages.success(self.request, "新規作成完了")
        return super().form_valid(form)

    def get(self, request):
        """管理人以外のアクセスはHTMLページでコメントを返す"""
        if not request.user.is_authenticated:
            return HttpResponse("<h1>権限がありません。</h1>")
        return super().get(request)


class EditBlogFormView(UpdateView):
    """更新用フォーム"""

    model = Blog
    form_class = BlogForm
    template_name = "blogs/edit_blog.html"
    success_url = reverse_lazy("blogs:index")
    get_object_name = "blog"

    def form_valid(self, form):
        """検証が終わったらメッセージを表示する"""
        messages.success(self.request, "更新完了")
        return super().form_valid(form)

    def get(self, request, pk):
        """管理人以外のアクセスはHTMLページでコメントを返す"""
        if not request.user.is_authenticated:
            return HttpResponse("<h1>権限がありません。</h1>")
        return super().get(request, pk)


def release(request, pk):
    """Blog公開用"""
    if request.user.is_authenticated:
        blog_release = get_object_or_404(Blog, id=pk, is_publick=False)
        blog_release.to_release()
        return redirect("blogs:index")
    return HttpResponse("<h1>権限がありません。</h1>")


def private(request, pk):
    """Blog非公開用"""
    if request.user.is_authenticated:
        blog_private = get_object_or_404(Blog, id=pk, is_publick=True)
        blog_private.to_private()
        return redirect("blogs:private_index")
    return HttpResponse("<h1>権限がありません。</h1>")


class CategoryGraphView(View):
    template_name = "blogs/edit_blog.html"

    def get(self, request):
        """Blogカテゴリーのグラフ"""

        # リンターで引っかかるので定義
        _ = japanize_matplotlib
        plt.rcParams.update({"figure.autolayout": True})
        fig = plt.figure(facecolor="whitesmoke")
        ax = fig.add_subplot(1, 1, 1)
        ax.set_facecolor("whitesmoke")  # プロット内の背景色

        # グラフの枠線を削除
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)

        # ラベルの補助線を削除
        plt.tick_params(bottom=False, left=False, right=False, top=False)

        """ここにデータを作成する"""
        category_choice = Category.objects.all()
        blogs_choice = Blog.objects.select_related("category").all()
        x1 = [data.title for data in category_choice]
        y1 = [data.category_id for data in blogs_choice]
        y1 = np.unique(y1, return_counts=True)
        colorlist = ["r", "y", "g", "b", "m", "c", "#ffff33", "#f781bf"]
        ax.bar(x1, y1[1], color=colorlist, width=0.3, alpha=0.5)
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(buf)
        response = HttpResponse(buf.getvalue(), content_type="image/png")
        fig.clear()
        response["Content-Length"] = str(len(response.content))

        # 引数requestがリンターで引っかかるので無理に定義しているだけ
        request.close()
        return response
