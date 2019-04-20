from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm


def blog_post_list_view(request):
	qs= BlogPost.objects.all()
	template_name= 'blog/list.html'
	context= {'object_list': qs}
	return render(request, template_name, context)


def blog_post_create_view(request):
	form= BlogPostModelForm(request.POST or None)
	if(form.is_valid()):
		obj= form.save(commit=False)
		#obj.title= form.cleaned_data.get("title") + "0"
		obj.save()
		#print(form.cleaned_data)
		#title= form.cleaned_data['title']
		#obj=BlogPost.objects.create(**form.cleaned_data)
		#obj2=OtherModel.objects.create(title=title)
		form=BlogPostModelForm()
	template_name= 'form.html'
	context= {'form': form}
	return render(request, template_name, context)



def blog_post_detail_view(request, slug):
	obj=get_object_or_404(BlogPost, slug=slug)
	template_name= 'blog/detail.html'
	context= {'object': obj}
	return render(request, template_name, context)



def blog_post_update_view(request, slug):
	obj= get_object_or_404(BlogPost, slug=slug)
	template_name= 'blog/update.html'
	context= {'object': obj, 'form': None}
	return render(request, template_name, context)



def blog_post_delete_view(request, slug):
	obj=get_object_or_404(BlogPost, slug=slug)
	template_name= 'blog/delete.html'
	context= {'object': obj}
	return render(request, template_name, context)
