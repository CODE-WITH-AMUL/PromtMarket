# from django.shortcuts import render
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.conf import messages
# from django.contrib.auth.models import User


# class LoginAcountView():
#     def get(self , request):
#         template_name = 'account/login.html'
#         return render(request, template_name)
    
#     def post(self , request):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         user = authenticate(request , email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect('/')
#         else:
#             messages.error(request, 'Invalid email or password')
#             return HttpResponseRedirect('/account/login/')
        

# class RegsiterView():
#     def get(self , request):
#         template_name = 'account/register.html'
#         return render(request, template_name)
    
#     def post(self , request):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         if password != confirm_password:
#             messages.error(request, 'Passwords do not match')
#             return HttpResponseRedirect('/account/register/')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists')
#             return HttpResponseRedirect('/account/register/')
        
#         user = User.objects.create_user(email=email, password=password)
#         user.save()
        
#         messages.success(request, 'Account created successfully')
#         return HttpResponseRedirect('/account/login/')
    
# @login_required
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect('/account/login/')

