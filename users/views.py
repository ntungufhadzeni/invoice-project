from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from users.forms import SignupForm


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
