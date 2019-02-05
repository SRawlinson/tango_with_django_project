from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.shortcuts import render
from django.http import HttpResponse
#import the Category model 
from rango.models import Category
from rango.models import Page

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors - 
            # Just print them to the terminal
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form}) 

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # context_dict = { 'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # Chapter 6:
    # Query the database for a list of ALL categories currently stored. 
    # Order the categories by no. of likes in descending order. 
    # Retrieve the top 5 only - or all if less than five.
    # PLace the list in our context_dict dictionary
    # that will be passed to the template engine. 

    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': pages_list} 


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier. 
    # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context_dict)
    

def about(request):
    context_dict = { 'boldmessage': "A less weird message."}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass 
    # to the template rendering engine. 
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception. 
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages. 
        # Note that filter() will return a list of page objects or an empty list. 
        pages = Page.objects.filter(category=category)

        #Adds our results list ot the template context under name pages 
        context_dict['pages'] = pages
        # We also add the category object form 
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists. 
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specificied cateogry. 
        # Don't do anything - 
        # the template will display the "no category" message for us. 
        context_dict['category'] = None
        context_dict['pages'] = None

    #Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to 
    # True when registration succeeds. 
    registered = False

    # If it's a HTTP POST, we're interested in processing form data. 
    if request.method == 'POST':
        # Attempt to grab information form the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid... 
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the databse.
            user = user_form.save()

            # Now we hash the password with the set_password method. 
            # Once hashed, we can update the user object. 
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance. 
            # Since we need to set the user attribute ourselves, 
            # we set commit=False. This delays saving the model
            # until we're ready ot avoid the integrity problems. 
            profile = profile_form.save(commit=False)
            profile.user = user 

            # Did the user provide a profile picture? 
            # If so, we need to get it from the input form and 
            # put it in the UserProfile model. 
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            # Now we save the UserProfile model instance. 
            profile.save()

            # Update our variable to indicate that the template 
            # registration was susccessful
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal. 
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances. 
        # These forms will be blank, ready for user input. 
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    # Render the template depending on the context. 
    return render(request,
                   'rango/register.html',
                   {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


