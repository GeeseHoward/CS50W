from django.shortcuts import render, redirect
from django import forms
import markdown2
from . import util
import random


class SearchForm(forms.Form):
    query = forms.CharField(label="Search Query")
    query.widget = forms.TextInput(attrs={'class': "search", 'type': "text", 'name': "q",
                                          'placeholder': "Search Encyclopedia"})


class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    md_content = forms.CharField(label="MD Content", widget=forms.Textarea)


class EditForm(forms.Form):
    md_content = forms.CharField(label="MD Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def get_entry(request, entry_title):
    entry_content = util.get_entry(entry_title)
    if not entry_content:
        return render(request, "encyclopedia/errors/not_found.html", {
            "entry_title": entry_title,
            "search_form": SearchForm()
        })
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "entry_content": markdown2.markdown(entry_content),
        "search_form": SearchForm()
    })


def search(request):
    search_form = SearchForm(request.POST)
    search_query = search_form['query'].value()

    all_entries = util.list_entries()

    if search_query in all_entries:
        return redirect("get_entry", entry_title=search_query)
    else:
        search_results = []
        for entry in all_entries:
            if search_query in entry:
                search_results.append(entry)
        if search_results:
            return render(request, "encyclopedia/search_results.html", {
                "entries": search_results,
                "search_form": SearchForm()
            })
        else:
            return render(request, "encyclopedia/errors/no_results.html", {
                "search_query": search_query,
                "search_form": SearchForm()
            })


def add_entry(request):
    if request.POST:
        entry_form = EntryForm(request.POST)
        entry_title = entry_form['title'].value()

        all_entries = util.list_entries()

        if entry_title not in all_entries:
            entry_md_content = entry_form['md_content'].value()
            util.save_entry(entry_title, entry_md_content)
            return redirect("get_entry", entry_title=entry_title)
        else:
            return render(request, "encyclopedia/errors/already_exists.html", {
                "entry_title": entry_title,
                "search_form": SearchForm()
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "entry_form": EntryForm(),
            "search_form": SearchForm()
        })


def edit_entry(request, entry_title):
    all_entries = util.list_entries()
    if entry_title not in all_entries:
        pass

    if request.POST:
        edit_form = EditForm(request.POST)
        entry_md_content = edit_form['md_content'].value()
        util.save_entry(entry_title, entry_md_content)
        return redirect("get_entry", entry_title=entry_title)
    else:
        entry_content = util.get_entry(entry_title)
        edit_form = EditForm(initial={"md_content":entry_content})
        return render(request, "encyclopedia/edit_entry.html", {
            "entry_title": entry_title,
            "edit_form": edit_form,
            "search_form": SearchForm()
        })


def random_entry(request):
    all_entries = util.list_entries()
    chosen_entry = random.choice(all_entries)
    return redirect("get_entry", entry_title=chosen_entry)
