from django.shortcuts import render
from .forms import SignUpForm, ContactForm
from django.core.mail import send_mail
from django.conf import settings
from .models import SignUp
# Create your views here.

def home(request):
	title = 'Sign Up Now'
	form = SignUpForm(request.POST or None)

	context = {
		"title": title,
		"form": form
		}
	if form.is_valid():
		instance = form.save(commit=False)
		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "Mr. Bekiyev"
		instance.full_name = full_name
		instance.save()
		context = {
			"title": "Thank you for submission. "
		}
	if request.user.is_authenticated() and request.user.is_staff:
		queryset = SignUp.objects.all().order_by('-timestamp')
		context = {
			"queryset": queryset
		}
	return render(request, "home.html", context)


def contact(request):
	title = "Contact Us"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		
		subject = 'Site Contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'bekiyev@gmail.com']
		contact_message = "%s: %s via %s" %(form_full_name, form_message, form_email)
		some_html_message = """ <h1> Hello There</h1> """
		send_mail(subject, contact_message, form_email, to_email, html_message=some_html_message, fail_silently=False)


	context = {
		"form": form,
		 "title": title,
		}
	return render(request, "forms.html", context)














