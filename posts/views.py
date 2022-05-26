from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Profile, Relationship, ProfileManager
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Create your views here.
@login_required
def post_comment_create_and_list_view(request):
    profile = Profile.objects.get(user=request.user)
    friends = Profile.objects.filter(friends=profile.user)
    pre_qs = []
    for item in friends:
        pre_qs.append(item.id)
    qs = Post.objects.filter(author__in=pre_qs)


    is_empty = False
    if len(qs)==0:
        is_empty = True
    p_form = PostModelForm()
    c_form = CommentModelForm()

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()


    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'is_empty': is_empty
    }

    return render(request, 'posts/main.html', context)


@login_required
def liked_posts_list_view(request):

    profile = Profile.objects.get(user=request.user)
    liked = Like.objects.filter(user=profile, value='Like').values_list('post_id', flat=True)
    pre_qs = []
    for item in liked:
        pre_qs.append(item)
    qs = Post.objects.filter(pk__in=pre_qs)

    c_form = CommentModelForm()
    is_empty = False
    if len(qs)==0:
        is_empty = True
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
    context = {
        'qs': qs,
        'profile': profile,
        'c_form': c_form,
        'is_empty': is_empty,
    }
    return render(request, 'posts/myfoodbook.html', context)



@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

            post_obj.save()
            like.save()
        else:
            like.value = 'Like'
            post_obj.save()
            like.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts:main-post-view')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('profile:my-profile-view')
    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'Вы должны быть автором рецепта что-бы удалить его.')
        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('profile:my-profile-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Вы должны быть автором рецепта что-бы изменить его.')
            return super().form_invalid(form)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/detail_post.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        print(pk)
        post = Post.objects.get(pk=pk)
        context['post'] = post
        return context


# class FoodBookDetailView(LoginRequiredMixin, DetailView):
#     model = Profile
#     template_name = 'posts/foodbook.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = Profile.objects.get(slug=self.request.path.split('/')[3])
#         liked = Like.objects.filter(user=profile, value='Like').values_list('post_id', flat=True)
#         qs = []
#         for item in liked:
#             qs.append(Post.objects.get(id=item))
#
#         c_form = CommentModelForm()
#         if 'submit_c_form' in self.request.POST:
#             print("Заходим")
#             c_form = CommentModelForm(self.request.POST)
#             if c_form.is_valid():
#                 instance = c_form.save(commit=False)
#                 instance.user = profile
#                 instance.post = Post.objects.get(id=self.request.POST.get('post_id'))
#                 instance.save()
#                 c_form = CommentModelForm()
#         context['profile'] = profile
#         context['qs'] = qs
#         if len(context['qs']) == 0:
#             context['is_empty'] = True
#         context['c_form'] = c_form
#
#         return context


@login_required
def food_book_detail_view(request, slug):
    profile = Profile.objects.get(slug=slug)
    liked = Like.objects.filter(user=profile, value='Like').values_list('post_id', flat=True)
    pre_qs = []
    is_empty = False
    for item in liked:
        pre_qs.append(item)
    qs = Post.objects.filter(pk__in=pre_qs)

    c_form = CommentModelForm()

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()

    if len(qs) == 0:
        is_empty = True

    context = {
        'qs': qs,
        'profile': profile,
        'c_form': c_form,
        'is_empty': is_empty,
    }
    return render(request, 'posts/foodbook.html', context)
