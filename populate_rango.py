import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    # First, we will create lists of dictionaries containing the page
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories. 
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models. 

    python_pages = [
        {"title": "Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greentapress.com/thinkpython/"},
        {"title":"Leanr Pyhton in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/"} ]
    
    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs/djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/"} ]
    
    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev"},
        {"title":"Flask",
        "url":"http://flask.pocoo.org"} ]
    

    # LAUREN! Here is the dictionary, I have no idea if this is formatted correctly cos I haven't really used dictionaries before
    # but my understanding is that category 'Python' cycles through the python_pages but gives each the same number of views on likes - 
    # I don't know why we want that. 
    cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64}, 
                "Django": {"pages": django_pages, "views":64, "likes":32},
            "Other Frameworks": {"pages": other_pages, "views":32, "likes":16} }

    #The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    # if you are using Python 2.x then use cats.iteritems() see
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/
    # for more information about how to iterate over a dictionary porperly


#22/01 - can't compile due to below arg: missing 2 required positional arguments
# 'views' and 'likes'. Can't work out where 'cat' is initialised or 
#the syntax for iterating over a dict with the comma? No idea really. Maybe cos of the nested loop? 

    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"])


    
    #Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p
#Updating this to take more inputs than the name has caused all the trouble! 
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    c.likes=likes
    c.views=views
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("starting Rango population script...")
    populate()
