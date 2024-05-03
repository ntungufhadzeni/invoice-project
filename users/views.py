from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from users.forms import SignupForm
from users.models import User


class UserSignupView(View):
    template_name = 'users/signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class EmailValidation(View):

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=self.request.POST["email"]).exists():
            return HttpResponse("<p class='errors' id='emailError'>The email already exists</p> \
                <button type='submit' class='btn btn-secondary ms-auto' id='submitBtn' hx-swap-oob='true' disabled>Register</button>")
        else:
            return HttpResponse("<p class='errors' id='emailError'></p> \
                <button type='submit' class='btn btn-primary ms-auto' id='submitBtn' hx-swap-oob='true'>Register</button> ")
