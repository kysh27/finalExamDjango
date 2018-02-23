from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from tablib import Dataset
from .forms import UserForm, ContactForm
from .models import AddressBook
from .resources import AddressResource

# Create your views here.
def index(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "This is the index page."}

    return render_to_response('addbook/index.html', context_dict, context)

def register(request):
    context = RequestContext(request)

    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If HTTP POST, process form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # hash the password with the set_password method.
            user.set_password(user.password)
            user.save()

            # registration was successful
            registered = True

        # Invalid forms
        else:
            print (user_form.errors)

    else:
        user_form = UserForm()

    return render_to_response(
            'addbook/register.html',
            {
                'user_form': user_form, 
                'registered': registered
            },
            context)


   
def user_login(request):
    context = RequestContext(request)
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # account is valid and active
                # send the user to the homepage
                login(request, user)
                print(username, user.is_authenticated)
                contacts = AddressBook.objects.filter(useridfk=request.user)
                return render(request, 'addbook/index.html', {'user': user, 'contacts': contacts})
            else:
                # inactive account
                return HttpResponse("Your account is disabled.")
        else:
            # invalid login details
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    #display the login form
    else:
        # blank dictionary object...
        return render_to_response('addbook/login.html', {}, context)


def home(request):
    contacts = AddressBook.objects.filter(useridfk=request.user)
    print ("model contact: " + str(contacts))
    return render(request, 'addbook/home.html', {'contacts': contacts})


def user_logout(request):
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "You are logged out"}

    return render_to_response('addbook/logout.html', context_dict, context)


def add_new(request):
    context = RequestContext(request)

    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            # Save the form data to the database.
            contact = contact_form.save(commit=False)
            contact.useridfk = request.user
            contact.save()
            return redirect('home')

        # Invalid forms
        else:
            print (contact_form.errors)

    else:
        contact_form = ContactForm()
    return render_to_response(
            'addbook/add.html',
            {
                'contact_form': contact_form,
            },
            context)


def post_edit(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    contact_form = ContactForm(request.POST or None, instance=contact)
    if contact_form.is_valid():
        contact_form.save()
        return redirect('home')
    return render(request, 'addbook/add.html', {'contact_form': contact_form})


def post_delete(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)    
    if request.method=='POST':
        contact.delete()
        return redirect('home')
    return render(request, 'addbook/delete.html', {'contact': contact})


def csv_import(request):
    if request.method == 'POST':
        contact_resource = AddressResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = contact_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            contact_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect('home')
        return redirect('home')

    return render(request, 'addbook/import.html')