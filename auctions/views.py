from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django import forms
import time
from .models import User, Listing, CategoryA, CategoryB, CategoryC, CATEGORY_MODEL, Image, Bid, Watchlist, Comment
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from crispy_forms.helper import FormHelper


class NewListingForm(forms.Form):

    CATEGORIES = (
        (CategoryA.get_id(), "CatA"),
        (CategoryB.get_id(), "CatB"),
        (CategoryC.get_id(), "CatC"),
    )
    title = forms.CharField(label="Title")
    desc = forms.CharField(label="Description", widget=forms.Textarea, max_length=512)
    price = forms.IntegerField(label="Price")
    image = forms.ImageField(required=False)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=CATEGORIES, required=False)
    helper = FormHelper()


class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")


class CommentForm(forms.Form):
    text = forms.CharField(label="Comment here")


class SelectCategoryForm(forms.Form):

    CATEGORIES = (
        (CategoryA.get_id(), "CatA"),
        (CategoryB.get_id(), "CatB"),
        (CategoryC.get_id(), "CatC"),
    )
    AND = 'AND'
    OR = 'OR'
    SEARCH_TYPE = [(AND, AND), (OR, OR)]
    search_type = forms.ChoiceField(label="Search Type", choices=SEARCH_TYPE, widget=forms.RadioSelect, initial=OR)
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                           choices=CATEGORIES, required=False, initial=CategoryA.get_id())


def index(request):
    listings = Listing.objects.all()
    active_listings = []
    for listing in listings:
        if listing.is_active is True:
            active_listings.append(listing)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            redirect_arg = request.POST.get("next") or reverse("index")
            return HttpResponseRedirect(redirect_arg)
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url=reverse_lazy("login"))
def create_listing(request):
    if request.POST:
        listing_form = NewListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            title = listing_form.cleaned_data.get("title")
            desc = listing_form.cleaned_data.get("desc")
            price = listing_form.cleaned_data.get("price")
            categories = listing_form.cleaned_data.get("categories")
            image = listing_form.cleaned_data.get("image")
            listing = Listing(seller=request.user, title=title, desc=desc, price=price,
                              date_created=time.strftime('%Y-%m-%d %I:%M %p'), is_active=True)
            with transaction.atomic():
                listing.save()
                if categories:
                    for category in categories:
                        category_class = CATEGORY_MODEL[category]
                        category_entry = category_class(listing=listing)
                        category_entry.save()
                if image:
                    img_entry = Image(image=image, listing=listing)
                    img_entry.save()
            return HttpResponseRedirect(reverse("index"))               # This can be made better
        else:
            return render(request, "auctions/errors/invalid_form.html")
    else:
        return render(request, "auctions/create_listing.html", {
            "listing_form": NewListingForm()
        })


def listings_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.POST:

        if not request.user.is_authenticated:
            login_url_base = reverse("login")
            params = urlencode({'next': reverse("listings_view", kwargs={'listing_id': listing_id})})
            redirect_url = '{}?{}'.format(login_url_base, params)
            return HttpResponseRedirect(redirect_url)

        if 'bid-submit' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = Bid(listing=listing, bidder=request.user, value=bid_form.cleaned_data.get('bid'))
                bid.save()
                return HttpResponseRedirect(reverse('listings_view', kwargs={'listing_id': listing_id}))
            else:
                return render(request, "auctions/errors/invalid_form.html")
        elif 'add-to-watchlist' in request.POST:
            watchlist_entry = Watchlist.objects.create(user=request.user, listing=listing)
            watchlist_entry.save()
            return HttpResponseRedirect(reverse('listings_view', kwargs={'listing_id': listing_id}))
        elif 'remove-from-watchlist' in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return HttpResponseRedirect(reverse('listings_view', kwargs={'listing_id': listing_id}))
        elif 'close-listing' in request.POST:
            listing.is_active = False
            listing.save()
            return HttpResponseRedirect(reverse('listings_view', kwargs={'listing_id': listing_id}))
        elif 'add-comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment_entry = Comment.objects.create(listing=listing, author=request.user,
                                                       text=comment_form.cleaned_data.get('text'),
                                                       date_added=int(time.time()))
                comment_entry.save()
            return HttpResponseRedirect(reverse('listings_view', kwargs={'listing_id': listing_id}))
    else:
        bid_form = BidForm()
        comment_form = CommentForm()
        max_bid = listing.bids.last()
        in_watchlist = False
        if request.user.is_authenticated:
            in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": bid_form,
            "max_bid": max_bid,
            "in_watchlist": in_watchlist,
            "comment_form": comment_form
        })


def watchlist_view(request):
    if request.user.is_authenticated:
        watchlist_items = Watchlist.objects.filter(user=request.user)
        watchlist_listings = [x.listing for x in watchlist_items]
        return render(request, "auctions/watchlist.html", {
            "listings": watchlist_listings
        })


def categories_view(request):
    if request.POST:
        select_category_form = SelectCategoryForm(request.POST)

        if select_category_form.is_valid():
            search_type = select_category_form.cleaned_data.get('search_type')
            categories = select_category_form.cleaned_data.get('categories')
            all_listings = Listing.objects.all()

            if search_type == select_category_form.AND:
                results = [x for x in all_listings]
                for listing in all_listings:
                    for category in categories:
                        category_class = CATEGORY_MODEL[category]
                        res = category_class.objects.filter(listing=listing)
                        if not res:
                            results.remove(listing)
                            break
            else:
                results = []
                for category in categories:
                    category_class = CATEGORY_MODEL[category]
                    for category_objects in category_class.objects.all():
                        if category_objects.listing not in results:
                            results.append(category_objects.listing)

            return render(request, "auctions/categories.html", {
                "select_category_form": select_category_form,
                "listings": results
            })
        else:
            return render(request, "auctions/errors/invalid_form.html")

    else:
        return render(request, "auctions/categories.html", {
            "select_category_form": SelectCategoryForm()
        })
