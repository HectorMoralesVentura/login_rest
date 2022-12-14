from django.shortcuts import render, redirect

from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from api.models import User
from rest_framework import status
from rest_framework.response import Response
from api.serializers import UserSerializer




class UserList(generics.ListCreateAPIView):
    
    #queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [IsAuthenticated]
    
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, *args, **kwargs):
        
        persona = User.objects.all()
        self.queryset = persona
        print(request.user)
        
        return self.list(request, *args, **kwargs)
    
#class UserList(generics.ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [IsAuthenticated]
#
#    def list(self, request):
#        # Note the use of `get_queryset()` instead of `self.queryset`
#        print(request.body)
#        print(request.data)
#        queryset = self.get_queryset()
#        serializer = UserSerializer(queryset, many=True)
#        return Response(serializer.data)


class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:user_list')
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)
        
    def form_valid(self, form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)


class Logout(APIView):
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)

