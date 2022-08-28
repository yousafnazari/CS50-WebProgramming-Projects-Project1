from http.client import HTTPResponse
from django import forms
from django.shortcuts import render, redirect
import random
from markdown2 import Markdown

from . import util

class NewForm(forms.Form):
    title = forms.CharField(label='Title and Content:', max_length=100, widget=forms.TextInput(attrs={
        'name': 'title', 'class': 'title'
    }))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'name': 'content', 'class': 'content'
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showEntry(request, name):
    name = name.lower()

    if name == "css" or name == "html" or name == "cs50":
        name = name.upper()
    else:
        name = name.title()

    if name not in util.list_entries():
        return render(request, "encyclopedia/entryNotFound.html", {
            "name": name
        })

    return render(request, "encyclopedia/showEntry.html", {
        "entry": Markdown().convert(util.get_entry(name)), "name": name
    })

def search(request):
    matchingEntries = []
    name = request.GET.get("q", "")
    name = name.lower()

    # check multiple conditions to format correctly
    if name == "css" or name == "html" or name == "cs50":
        name = name.upper()
    else:
        name = name.title()

    # check every entry in database for match
    for entry in util.list_entries():
        # if there is an exact match then go to entry page
        if entry == name:
            return redirect('encyclopedia:showEntry', name)
        
        # if there is a partial match then add to matching list
        if name.lower() in entry.lower():
            matchingEntries.append(entry)
    
    # if there are no matches, then go to entry not found page
    if not matchingEntries:
        return render(request, "encyclopedia/entryNotFound.html", {
            "name": name
        })
    else:
        # else go to search results page and display list of matching entries
        return render(request, "encyclopedia/searchResults.html", {
            "name": name, "matchingEntries": matchingEntries
        })

def newPage(request):
    form = NewForm()

    return render(request, "encyclopedia/newPage.html", {
        "form": form
    })

def saveNewEntry(request):
    # get title
    newEntryTitle = request.POST.get("title", "")

    match = False
    # check if title already exists in list of entries
    for entry in util.list_entries():
        if newEntryTitle.lower() == entry.lower():
            match = True
            break

    # if there was a match, then go to error page
    if match:
        return render(request, "encyclopedia/entryExistsError.html", {
            "name": newEntryTitle
        })
    else:
        # else if no match then continue to saving entry
        # get content
        newEntryContent = request.POST.get("content", "")

        util.save_entry(newEntryTitle, newEntryContent)
        
        return redirect("encyclopedia:showEntry", newEntryTitle)

def editEntry(request, name):
    # get entry first
    entry = Markdown().convert(util.get_entry(name))

    # go to edit entry page
    return render(request, "encyclopedia/editPage.html", {
        "name": name, "entry": entry
    })

def saveEdit(request, name):
    # get edited content
    content = request.POST.get("content", "")

    # save content
    util.save_entry(name, content)

    # show page with edit
    return redirect("encyclopedia:showEntry", name)

def randomPage(request):
    # use choice function to get random entry to display
    entry = random.choice(util.list_entries())

    # redirect to show entry
    return redirect("encyclopedia:showEntry", entry)