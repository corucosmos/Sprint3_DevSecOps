import logging
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core import mail, validators, serializers
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register

from django.http import HttpResponse, HttpResponseRedirect
from seng406_unsecure import settings as SETTINGS

from authentication.models import UserProfile, UserAddress
from main.forms import PostForm, ChangePasswordForm, EditProfileForm, EditAddressForm
from main.models import Post

logger = logging.getLogger(__name__)


@login_required(login_url='/login/')
def home(request):
    all_chat_profiles = UserProfile.objects.all()

    all_posts = Post.objects.order_by('-created_date').all()
    all_post_profiles = dict()
    for post in all_posts:
        all_post_profiles[post.id] = UserProfile.objects.get(user_id=post.user_id)

    if 'q' in request.GET and request.GET['q']:
        query = request.GET.get('q')
        all_posts = Post.objects.order_by('-created_date').filter(Q(text__icontains=query)).all()

    return render(request, 'newsfeed.html', context={'all_posts': all_posts,
                                                     'all_post_profiles': all_post_profiles,
                                                     'all_chat_profiles': all_chat_profiles
                                                     })


@login_required(login_url='/login/')
def settings(request):
    all_chat_profiles = UserProfile.objects.all()
    return render(request, 'settings.html', context={'all_chat_profiles': all_chat_profiles})


@login_required(login_url='/login/')
def payment_methods(request):
    user = request.user
    if user is not None and user.is_superuser:
        all_chat_profiles = UserProfile.objects.all()
        return render(request, 'payment_methods.html', context={'all_chat_profiles': all_chat_profiles})
    else: 
        return render(request, "403.html", {"msg": "Invalid credentials"})


@login_required(login_url='/login/')
def analytics(request):
    all_chat_profiles = UserProfile.objects.all()
    return render(request, 'analytics.html', context={'all_chat_profiles': all_chat_profiles})


@login_required(login_url='/login/')
def user_profile(request, user_id):
    all_chat_profiles = UserProfile.objects.all()

    retrieved_user_profile = UserProfile.objects.get(user_id=user_id)
    retrieved_user_posts = Post.objects.filter(Q(user_id=user_id)).all()
    retrieved_user_address = UserAddress.objects.filter(user_id=user_id).first()

    return render(request, 'user-profile.html',
                  context={'user_profile': retrieved_user_profile, 'user_posts': retrieved_user_posts,
                           'user_address': retrieved_user_address, 'all_chat_profiles': all_chat_profiles}
                  )


@login_required(login_url='/login/')
def create_post(request):
    all_chat_profiles = UserProfile.objects.all()

    if request.method == "POST":
        print(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form_post = form.save(commit=False)
            print(form_post.text)
            form_post.user = request.user
            form_post.save()
            print("SAVED POST")
            return HttpResponseRedirect("/")
    else:
        form = PostForm()

    return render(
        request, 'create_post.html', context={'form': form, 'all_chat_profiles': all_chat_profiles})


@login_required(login_url='/login/')
def help(request):
    all_chat_profiles = UserProfile.objects.all()

    if request.method == "GET":
        return render(request, 'help.html', context={"additional_info": "",
                                                     'all_chat_profiles': all_chat_profiles})
    else:
        file = request.POST['additional-info']
        try:
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, file)
            file = open(filename, "r")
            data = file.read()
            return render(request, "help.html", {"additional_info": "",
                                                 'all_chat_profiles': all_chat_profiles})
        except:
            return render(request, "help.html", {"additional_info": "",
                                                 'all_chat_profiles': all_chat_profiles})

@login_required(login_url='/login/')
def change_password(request):
    all_chat_profiles = UserProfile.objects.all()
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        user = request.user
        if form.is_valid() and user is not None:
            if form.cleaned_data["password1"] == form.cleaned_data["password2"]:
                try:
                    if validate_password(form.cleaned_data["password1"], user) is None:
                        user.set_password(form.cleaned_data["password1"])
                        user.save()
                        return HttpResponseRedirect("/")
                except ValidationError as ex:
                    for error in ex.error_list:
                        form.add_error("password2", error)
            else:
                form.add_error("password2", "Passwords don't match")
        else:
            logger.debug(form.data)

    else:
        form = ChangePasswordForm()

    return render(request, "change-password.html", {"form": form,
                                                    'all_chat_profiles': all_chat_profiles})


def all_profiles(request):
    user_profiles = UserProfile.objects.all()

    return render(request, "all-profiles.html", context={'user_profiles': user_profiles,
                                                         'all_chat_profiles': user_profiles})


@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user
    user_id = user.id
    all_chat_profiles = UserProfile.objects.all()
    logger.info("GET/POST (edit) profile for %s", user_id)
    profile = get_object_or_404(UserProfile, pk=user_id)

    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():

            profile_form.save()
            logger.info("Saved new profile data for user %s", profile.user.username)

        else:
            logger.debug(profile_form.errors)
            return render(
                request,
                "edit-profile.html",
                {"form": profile_form, "user": profile.user, "msg": "Error/s in form"},
            )

    profile = UserProfile.objects.filter(user_id=user_id).first()
    profile_form = EditProfileForm(instance=profile)

    return render(request, "edit-profile.html", context={'user_profile': profile, 'form': profile_form,
                                                         'all_chat_profiles': all_chat_profiles})


@login_required(login_url='/login/')
def edit_address(request):
    all_chat_profiles = UserProfile.objects.all()
    logger.info("GET/POST (edit) address for %s", request.user.id)
    address = UserAddress.objects.filter(user_id=request.user.id).first()
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        if address is None:
            address = UserAddress()
            address.user = request.user

        address_form = EditAddressForm(request.POST, request.FILES, instance=address)

        if address_form.is_valid():

            query = ("select * from authentication_useraddress where user_id != "
                     + str(request.user.id) + " AND street like '" + address_form.data['street'] + "'")
            result = UserAddress.objects.raw(query)

            if len(result) > 0:
                return render(
                    request,
                    "edit-address.html",
                    {"form": address_form, "msg": "Two users cannot share the same street address",
                     'all_chat_profiles': all_chat_profiles},
                )

            address_form.save()
            logger.info("Saved new address data for user %s", request.user.id)
            send_confirmation_email(user.email)

        else:
            logger.debug(address_form.errors)
            return render(
                request,
                "edit-address.html",
                {"form": address_form, "msg": "Error/s in form", 'all_chat_profiles': all_chat_profiles},
            )

    address = UserAddress.objects.filter(user_id=request.user.id).first()
    address_form = EditAddressForm(instance=address)

    return render(request, "edit-address.html", context={
        'form': address_form, 'all_chat_profiles': all_chat_profiles
    })


def send_confirmation_email(to_email):
    print("hello")
    to_send = mail.EmailMessage(
        "Address Update Success",
        "Thank you for using S406-Unsecure. Your address has now been updated.",
        "seng406@unsecure.app",
        [to_email]
    )
    to_send.send()


def events(request):
    all_chat_profiles = UserProfile.objects.all()
    return render(request, 'events.html', context={'all_chat_profiles': all_chat_profiles})


@register.filter
def image_from_dict(dict, key):
    return dict[key].profile_image


def debug_settings(request):
    if "S406Debug" in request.headers and request.headers["S406Debug"] == SETTINGS.TRUSTED_DEBUG_SECRET:
        with open(os.path.join(SETTINGS.BASE_DIR, 'seng406_unsecure/settings.py'), "r") as f:
            content = f.read()
        response = HttpResponse(content, "text/plain")
        return response

    return render(request, "403.html", {"msg": "Invalid header"})


@register.filter
def image_url_from_dict(dict, key):
    return dict[key].profile_image.url


def custom_404_view(request, exception):
    return render(request, '404.html')


def custom_500_view(request):
    return render(request, '500.html')
