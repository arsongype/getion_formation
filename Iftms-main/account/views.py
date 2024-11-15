from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'le nom utilisateur déjà existe')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email déjà existe')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Compte creér avec success')
                return redirect('login')
        else:
            messages.error(request, 'Confirmer votre mot de pass')

    return render(request, 'signup.html')

@login_required(login_url='login')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'connections reussite avec success') 
            return redirect('home')  # Redirect to home or dashboard after login
        else:
            messages.error(request, 'votre mot de passe ou nom utilisateur est incorect')

    return render(request, 'login.html')


@login_required(login_url='login')
def confirm_email(request, token):
    try:
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = None  # Supprime le token après confirmation
        user.save()
        messages.success(request, "Email confirmé ! Vous pouvez maintenant vous connecter.")
    except User.DoesNotExist:
        messages.error(request, "Lien invalide ou expiré.")

    return redirect("login")

@login_required(login_url='login')
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            token = get_random_string(32)
            user.token = token
            user.save()

            reset_url = f"{settings.BASE_URL}/reset_password/{token}/"
            send_mail(
                "Réinitialisation de mot de passe",
                f"Veuillez cliquer sur le lien pour réinitialiser votre mot de passe : {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            messages.success(request, "Vérifiez votre e-mail pour un lien de réinitialisation.")
        except User.DoesNotExist:
            messages.error(request, "Aucun compte associé à cet email.")
        return redirect("login")

    return render(request, "password_reset_request.html")



@login_required(login_url='login')
def reset_password(request, token):
    try:
        user = User.objects.get(token=token)
        if request.method == "POST":
            password = request.POST.get("password")
            user.password = password
            user.token = None
            user.save()
            messages.success(request, "Mot de passe réinitialisé avec succès !")
            return redirect("login")
    except User.DoesNotExist:
        messages.error(request, "Lien invalide ou expiré.")

    return render(request, "reset_password.html", {"token": token})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Supprime l'utilisateur de la session
        messages.success(request, "Vous êtes déconnecté.")
    return redirect("login")


# def logout(request):
#     auth_logout(request)
#     return redirect('logout')