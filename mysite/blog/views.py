from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.views import generic

from .forms import PostForm, PostImageForm
from .models import Post, PostImage
from account.models import Contact


class PostUserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostUserListView, self).get_context_data(**kwargs)
        all_users_except_self = User.objects.filter(is_staff=False).exclude(id=self.request.user.id).order_by('username')
        following_users = Contact.objects.filter(user_from=self.request.user).values_list('user_to_id', flat=True)
        users_to_suggest = User.objects.filter(is_staff=False).exclude(id__in=following_users).exclude(
            id=self.request.user.id).order_by('username')

        context.update({
            'all_users': all_users_except_self,
            'users_to_suggest': users_to_suggest,
        })
        return context

    def get_queryset(self):
        return Post.published.all().prefetch_related('tags', 'images')


@login_required
def post_create(request):
    PostImageFormSet = modelformset_factory(PostImage, form=PostImageForm, extra=3)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_formset = PostImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            post_form.save_m2m()

            for form in image_formset.cleaned_data:
                if form:
                    image = form['image']
                    PostImage(post=post, image=image).save()

            messages.success(request, 'Your post was successfully created!')
            return redirect('blog:post_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        post_form = PostForm()
        image_formset = PostImageFormSet(queryset=PostImage.objects.none())

    return render(request, "blog/post_create.html", context={"post_form": post_form, "image_formset": image_formset})


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

    data = {
        'liked': liked,
        'number_of_likes': post.likes.count()
    }
    return JsonResponse(data)
