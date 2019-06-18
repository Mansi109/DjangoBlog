from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm
#from django.http import Http404
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .otp import SendOtp, VerifyOtp
from django.contrib.auth.models import User
#from .serializers import BlogPostSerializer

def blog_post_list_view(request):
	qs= BlogPost.objects.all()
	template_name= 'blog/list.html'
	context= {'object_list': qs}
	return render(request, template_name, context)


@staff_member_required
#@login_required
# return.user -> return something
def blog_post_create_view(request):
	#if not request.user.is_authenticated:
	#	return render(request, "not-a-user.html", {})
	form= BlogPostModelForm(request.POST or None)
	if(form.is_valid()):
		obj= form.save(commit=False)
		obj.user=request.user
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


@staff_member_required
def blog_post_update_view(request, slug):
	obj= get_object_or_404(BlogPost, slug=slug)
	form= BlogPostModelForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()	
	template_name= 'form.html'
	context= {'form': form, "title": f"Update {obj.title}"}
	return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
	obj=get_object_or_404(BlogPost, slug=slug)
	template_name= 'blog/delete.html'
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context= {'object': obj}
	return render(request, template_name, context)



class Example(APIView): 

	def post(self, request, format = None):
		mobile= request.POST['mobile']
		#print(mobile)

		if len(mobile)!=10:
			mobile_error_dict = {
			"status":"error",
			"message":"number invalid"
			}
			return Response(data = mobile_error_dict)
		user_obj = User.objects.filter(username=mobile)
		if user_obj.exists():
			otp = SendOtp(mobile)
			if otp==0:
				dict = {
				"status":"error",
				"message":"msg91 service down"
				}
				return Response(data = dict)
			
			success_dict = {
		    "status":"success",
			"message":"otp sent successfully",
			# "data":{
			# 	    "otp":otp,
			#     	"user_id":user_obj[0].pk
			# 	}
			}
			return Response(data = success_dict)
		else:
			error_dict = {
		    "status":"error",
		    "message":"user with this mobile number doesn't exist in database"
		    }
			return Response(data = error_dict)



class Verify(APIView):

	def post(self, request, format = None):
		mobile = request.POST['mobile']
		otp = request.POST['otp']
		if len(mobile)!=10:
			mobile_error_dict = {
			"status":"error",
			"message":"number invalid"
			}
			return Response(data = mobile_error_dict)
		user_obj = User.objects.filter(username=mobile)
		if user_obj.exists():
			result = VerifyOtp(mobile,otp)
			if result==-1:
				dict = {
				"status":"error",
				"message":"msg91 service down"
				}
				return Response(data = dict)
			elif result == 0 :
				mismatch_dict = {
				"status":"error",
				"message":"otp mismatch error"
				}
				return Response(data = mismatch_dict)
			elif result == 1:
				success_dict = {
		    	"status":"success",
				"message":"otp confirmation successful",
				"data":{
				    	"otp":otp,
			    		"user_id":user_obj[0].pk
					}
				}
				return Response(data = success_dict)
		else:
			error_dict = {
		    "status":"error",
		    "message":"user with this mobile number doesn't exist in database"
		    }
			return Response(data = error_dict)



class ListView(APIView):
	def get(self, request, format=None):
		_id = request.GET.get('id')
		if _id is None:
			return Response({'status':'error', 'msg':'enter user id'})
		users = User.objects.filter(id=_id).values()

		return Response({'status':'success', 'data':users})





			


		

