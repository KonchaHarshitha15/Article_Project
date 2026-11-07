from django.shortcuts import render
from django.http import HttpResponse
from blog.models import post
from blog.forms import RegisterForm, UserUpdateForm, ProfileUpdateForm


from django.views.generic import (
    ListView, CreateView,DetailView, DeleteView,UpdateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class PostListView(LoginRequiredMixin,ListView):
    model=post
    context_object_name='posts'
    template_name = 'blog/home.html'

    ordering = ['-date_posted']
    paginate_by = 2

class PostCreateView(LoginRequiredMixin,CreateView):
    model=post
    fields=['title','content']
    context_object_name='form'
    template_name = 'blog/form_create.html'


    login_url='/login'



    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model=post
    context_object_name='post'
    template_name = 'blog/form_detail.html'

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=post
    fields=['title','content']
    context_object_name = 'form'
    template_name = 'blog/form_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=post
    context_object_name = 'post'
    template_name = 'blog/form_delete.html'

    login_url='/login'

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def handle_no_permission(self):
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name()
        )

class UserPostListView(LoginRequiredMixin,ListView):
    model=post
    context_object_name='user_posts'
    template_name='blog/user_post.html'
    ordering = ['-date_posted']

    def get_queryset(self):
        username = self.kwargs.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.user_not_found = True
            self.requested_username = username
            return post.objects.none()
        return post.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_not_found'] = getattr(self, 'user_not_found', False)
        context['requested_username'] = getattr(self, 'requested_username', None)
        return context


    '''def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return post.objects.filter(author=user)'''


def about_view(request):
    return render(request,'blog/about.html')



class LatestPostListView(ListView):
    model = post
    template_name = 'blog/latest_posts.html'
    context_object_name = 'latest_posts'


    def get_queryset(self):
        return post.objects.all().order_by('-date_posted')[:3]
    paginate_by = 2


def services_view(request):
    return render(request,'blog/services.html')




'''def home_page(request):
    posts = post.objects.all()

    context={
        'posts':posts
    }
    return render(request,'blog/home.html',context)
'''

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def logout_page(request):
    logout(request)
    return render(request,'blog/logout.html')

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST.get('username')
            messages.success(request,f'Account created for {username} successfully!')
            return redirect('login')

        else:
            username=request.POST.get('username')
            messages.warning(request,f'Account was not created for {username}.Please try again!')
            return redirect('register')
    else:
        form=RegisterForm()
        context={
            'form':form
        }
        return render(request,'blog/register.html',context)


from blog.models import Profile

@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'blog/profile.html', context)

'''@login_required(login_url='login')
def profile_view(request):
    if request.method=='POST':
        pass
    else:
        context={
            'user':request.user
        }
        return render(request,'blog/profile.html',context)

'''