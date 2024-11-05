from django.http import HttpResponseRedirect
from django.db.models import Q, Sum
from django.utils import timezone
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def Home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def Base(request):
    return render(request, 'base.html')


# ----------------------------------------------------------------          ---------------------------------------------------------------------
#                                                             full date the formateur
#----------------------------------------------------------------          -----------------------------------------------------------------------


@login_required(login_url='login')
def formateur_list(request):
    query = request.GET.get('q')  # Récupérer le terme de recherche depuis la requête
    if query:
        formateurs = Formateur.objects.filter(
            names__icontains=query
        ) | Formateur.objects.filter(
            last_name__icontains=query
        ) | Formateur.objects.filter(
            e_mail__icontains=query
        )
    else:
        formateurs = Formateur.objects.all()  # Si aucune recherche, afficher tous les formateurs
    
    return render(request, 'format/formateur_list.html', {'formateurs': formateurs, 'query': query})




@login_required(login_url='login')
def add_formateur(request):
    if request.method == 'POST':
        genr = request.POST.get('genr')
        names = request.POST.get('names')
        last_name = request.POST.get('last_name')
        e_mail = request.POST.get('e_mail')

        if genr and names and last_name and e_mail:
            Formateur.objects.create(genr=genr, names=names, last_name=last_name, e_mail=e_mail)
            messages.success(request, "Formateur ajouté avec succès !")
            return redirect(reverse('formateur_list'))
        else:
            messages.error(request, "Erreur: Tous les champs sont obligatoires.")
    return render(request, 'format/add_formateur.html')





@login_required(login_url='login')
def edit_formateur(request, id):
    formateur = get_object_or_404(Formateur, id=id)

    if request.method == 'POST':
        formateur.genr = request.POST.get('genr')
        formateur.names = request.POST.get('names')
        formateur.last_name = request.POST.get('last_name')
        e_mail = request.POST.get('e_mail')
        formateur.save()
        messages.success(request, "Formateur modifié avec succès !")
        return redirect(reverse('formateur_list'))
    return render(request, 'format/edit_formateur.html', {'formateur': formateur})



@login_required(login_url='login')
def formateur_delete(request, id):
    formateur = get_object_or_404(Formateur, pk=id)
    formateur.delete()
    messages.success(request, 'Formateur supprimé avec succès.')
    return redirect(reverse('formateur_list'))



# ----------------------------------------------------------------          ---------------------------------------------------------------------
#                                                             ful date the student
#----------------------------------------------------------------          -----------------------------------------------------------------------



@login_required(login_url='login')
def Stud(request):
    query = request.GET.get('q')  # Récupérer le terme de recherche depuis la requête
    if query:
        students = Student.objects.filter(
            nom__icontains=query
        ) | Student.objects.filter(
            prenom__icontains=query
        ) | Student.objects.filter(
            email__icontains=query
        )
    else:
        students = Student.objects.all()  # Si aucune recherche, afficher tous les étudiants
    
    return render(request, 'stud/stude.html', {'students': students, 'query': query})




@login_required(login_url='login')
def Add(request):
    formateurs = Formateur.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        naissance = request.POST.get('naissance')
        genre = request.POST.get('genre')
        email = request.POST.get('email')
        formateur_id = request.POST.get('formateur')

        # Check required fields
        if not (nom and prenom and naissance and genre and email and formateur_id):
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            formateur = Formateur.objects.get(id=formateur_id)
            student = Student(
                nom=nom,
                prenom=prenom,
                naissance=naissance,
                genre=genre,
                email=email,
                formateur=formateur
            )
            student.save()
            messages.success(request, "Étudiant ajouté avec succès !")
            return redirect(reverse('stude'))
    return render(request, 'stud/add.html', {'formateurs': formateurs})





@login_required(login_url='login')
def update(request, id):
    student = get_object_or_404(Student, id=id)
    formateurs = Formateur.objects.all()
    if request.method == 'POST':
        student.nom = request.POST.get('nom')
        student.prenom = request.POST.get('prenom')
        student.naissance = request.POST.get('naissance')
        student.genre = request.POST.get('genre')
        student.email = request.POST.get('email')
        formateur_id = request.POST.get('formateur')

        if formateur_id:
            student.formateur = Formateur.objects.get(id=formateur_id)
        student.save()
        messages.success(request, "Étudiant modifié avec succès !")
        return redirect(reverse('stude'))
    return render(request, 'stud/update.html', {'student': student, 'formateurs': formateurs})



@login_required(login_url='login')
def delete_student(request, id):
    student = get_object_or_404(Student, pk=id)
    student.delete()
    messages.success(request, 'Étudiant supprimé avec succès')
    return redirect(reverse('stude'))


# ----------------------------------------------------------------          ---------------------------------------------------------------------
#                                                             full date the formations
#----------------------------------------------------------------          -----------------------------------------------------------------------



@login_required(login_url='login')
def list_formations(request):
    query = request.GET.get('q')  # Récupérer le terme de recherche depuis la requête
    if query:
        formations = Formation.objects.filter(
            type__icontains=query
        ) | Formation.objects.filter(
            dure__icontains=query
        ) | Formation.objects.filter(
            prix__icontains=query
        )
    else:
        formations = Formation.objects.all()  # Si aucune recherche, afficher toutes les formations
    
    return render(request, 'for/form_liste.html', {'formations': formations, 'query': query})






@login_required(login_url='login')
def add_formation(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        dure = request.POST.get('dure')
        prix = request.POST.get('prix')
        if type and dure and prix:
            Formation.objects.create(type=type, dure=dure, prix=prix)
            messages.success(request, 'Formation ajouté avec succès.')
            return redirect(reverse_lazy('list_formations')) 
        else:
            messages.error(request, 'Please fill out all fields.')

        return render(request, 'for/add_form.html')





@login_required(login_url='login')
def update_formation(request, id):
    formation = get_object_or_404(Formation, id=id)

    if request.method == 'POST':
        formation.type = request.POST.get('type')
        formation.dure = request.POST.get('dure')
        formation.prix = request.POST.get('prix')

        formation.save()
        messages.success(request, 'Formation modifié avec succès.')
        return redirect(reverse_lazy('list_formations')) 

    return render(request, 'for/edit_form.html', {'formation': formation})




@login_required(login_url='login')
def delete_formation(request, id):
    formation = get_object_or_404(Formation, pk=id)
    formation.delete()
    messages.success(request, 'Formation supprimé avec succès.')
    return redirect('list_formations')



# ----------------------------------------------------------------          ---------------------------------------------------------------------
#                                                             ful date the inscriptions
#----------------------------------------------------------------          -----------------------------------------------------------------------



@login_required(login_url='login')
def inscrie_list(request):
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Base query for inscriptions
    query = Inscrie.objects.select_related('student', 'formation')

    if search_query:
        query = query.filter(
            Q(student__nom__icontains=search_query) |
            Q(student__prenom__icontains=search_query) |
            Q(student__email__icontains=search_query) |
            Q(formation__type__icontains=search_query)
        )

    if start_date and end_date:
        query = query.filter(dates__range=[start_date, end_date])

    inscries = query

    # Calculate total price of all inscriptions
    total_price = inscries.aggregate(Sum('formation__prix'))['formation__prix__sum'] or 0

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('ins/partials/inscrie_list.html', {
            'inscries': inscries,
            'total_price': total_price,
        })
        return JsonResponse({'html': html})

    return render(request, 'ins/liste_inscrie.html', {
        'inscries': inscries,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'total_price': total_price,
    })



#---------------------------------------------------------------- --------------------------------


@login_required(login_url='login')
def add_inscrie(request):
    students = Student.objects.all()
    formations = Formation.objects.all()

    if request.method == 'POST':
        dates = request.POST.get('dates')
        student_id = request.POST.get('student')
        formation_id = request.POST.get('formation')

        student = get_object_or_404(Student, id=student_id)
        formation = get_object_or_404(Formation, id=formation_id)

        inscrie = Inscrie(dates=dates, student=student, formation=formation)
        inscrie.save()
        
        # Send confirmation email
        # send_mail(
        #     'Confirmation d’inscription',
        #     f'Bonjour {student.nom} {student.prenom},\n\n'
        #     f'Vous êtes inscrit à la formation "{formation.type}" d’une durée de {formation.dure} mois le "{inscrie.dates}. '
        #     f'Le coût de la formation est {formation.prix} Ariary.\n\n'
        #     'Merci pour votre inscription.',
        #     'gype09@gmail.com',  # Replace with your sender email
        #     [student.email],  # Student's email as the recipient
        #     fail_silently=False,
        #     
        #     )
        messages.success(request, 'Inscription ajouté avec succès')
        return redirect(reverse('liste_inscrie'))

    return render(request, 'ins/add_inscription.html', {'students': students, 'formations': formations})

#---------------------------------------------------------------- fin --------------------------------



@login_required(login_url='login')
def edit_inscrie(request, id):
    inscrie = get_object_or_404(Inscrie, id=id)
    students = Student.objects.all()
    formations = Formation.objects.all()

    if request.method == 'POST':
        inscrie.dates = request.POST.get('dates')
        student_id = request.POST.get('student')
        formation_id = request.POST.get('formation')
        
        inscrie.student = get_object_or_404(Student, id=student_id)
        inscrie.formation = get_object_or_404(Formation, id=formation_id)
        inscrie.save()

        messages.success(request, 'Inscription modifié avec succès')
        return redirect(reverse('liste_inscrie'))

    return render(request, 'ins/inscrie_update.html', {
        'inscrie': inscrie, 
        'students': students, 
        'formations': formations
    })
#---------------------------------------------------------------- fin ----------------------------------------------------------------



@login_required(login_url='login')
def delete_inscrie(request, id):
    inscrie = get_object_or_404(Inscrie, pk=id)
    inscrie.delete()
    messages.success(request, 'Inscription supprimé avec succès')
    return redirect('liste_inscrie')

#------------------------------------------------ fin all -----------------------------------------------


# ----------------------------------------------------------------          ---------------------------------------------------------------------
#                                                             generation de pdf inscriptions
#----------------------------------------------------------------          -----------------------------------------------------------------------

def generate_pdf(request, inscrie_id):
    inscrie = get_object_or_404(Inscrie, id=inscrie_id)

    # Préparer le contexte pour le template
    context = {
        'inscrie': inscrie,
        'student': inscrie.student,
        'formation': inscrie.formation,
    }

    # Render le template HTML en PDF
    template_path = 'ins/generate_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Inscription_{inscrie.id}.pdf"'
    html = render_to_string(template_path, context)

    # Créer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Vérifie s'il y a des erreurs
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)

    return response


