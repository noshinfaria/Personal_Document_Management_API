from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator

from .forms import FileUploadForm, UserShareForm
from .models import FileUpload, FileShare
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import os
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
# @login_required
def document_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_up = form.save(commit=False)
            fileName, fileExtension = os.path.splitext(new_up.file.name)
            print(fileExtension)
            new_up.file_formate = fileExtension
            new_up.author = request.user
            new_up.save()
        else:
            context = {'form': form}
            return render(request, "document/documentupload.html", context)
    context = {
        'form': FileUploadForm()
    }
    return render(request, "document/documentupload.html", context)


# def document_list(request):
#     list = FileUpload.objects.filter(author=request.user)
#     context = {
#         'list': list
#     }
#     return render(request, "document/document_list.html", context)


class document_list(ListView, APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    context_object_name = 'list'
    model = FileUpload
    template_name = 'document/document_list.html'
    paginate_by = 2

    def get_queryset(self):
        filter_val = self.request.GET.get("filter", "")
        order_by = self.request.GET.get("orderby", "id")
        if filter_val != "":
            cat = FileUpload.objects.filter(
                Q(title__contains=filter_val)
                | Q(upload_date__contains=filter_val)
                | Q(description__contains=filter_val)
                | Q(file_formate__contains=filter_val)).order_by(order_by)
        else:
            cat = FileUpload.objects.filter(author=self.request.user).order_by(order_by)

        return cat

    def get_context_data(self, **kwargs):
        context = super(document_list, self).get_context_data(**kwargs)
        context["filter"] = self.request.GET.get("filter", "")
        context["orderby"] = self.request.GET.get("orderby", "id")
        context["all_table_fields"] = FileUpload._meta.get_fields()
        return context

    def test_func(self):
        fileupload = self.get_object()
        return self.request.user == fileupload.author


@method_decorator(csrf_exempt, name='dispatch')
class PostEditView(UserPassesTestMixin, UpdateView):
    model = FileUpload
    fields = ['title', 'file', 'description']
    template_name = 'document/post_edit.html'

    def get_success_url(self):
        # pk = self.kwargs['pk']
        return reverse_lazy('list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@csrf_exempt
def delete_file(request, pk):
    uploadfile = get_object_or_404(FileUpload, pk=pk)
    uploadfile.delete()
    return redirect('list')


class Shared_user(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *arg, **kwargs):
        file = FileUpload.objects.get(pk=pk)
        form = UserShareForm()

        shares = FileShare.objects.filter(file=file)

        context = {
            'file': file,
            'form': form,
            'shares': shares,
        }
        return render(request, 'document/shared_user.html', context)

    def post(self, request, pk, *args, **kwargs):
        file = FileUpload.objects.get(pk=pk)
        form = UserShareForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            existing_user = FileShare.objects.filter(Q(file=file, share_with_id=new_comment.share_with))
            if existing_user:
                messages.error(request, "Already shared this file with this person")
            else:
                new_comment.file = file
                new_comment.save()

        shares= FileShare.objects.filter(file=file)

        context = {
            'file': file,
            'form': form,
            'shares': shares,
        }
        return render(request, 'document/shared_user.html', context)


def shared_file(request):
    sharedfile = FileShare.objects.filter(share_with=request.user)
    context = {
        'sharedfile': sharedfile
    }
    return render(request, "document/shared_file.html", context)