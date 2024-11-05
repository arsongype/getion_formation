from django.urls import path,include
from .views import *

urlpatterns = [
    path('home/',Home, name='home'),
    path('base/',Base, name='base'),
    
    
    
    
    ################################ 
    
    
    path('formateur_list/',formateur_list, name='formateur_list'),
    path('add_formateur/',add_formateur, name='add_formateur'),
    path('edit_formateur/<int:id>/',edit_formateur, name='edit_formateur'),
    path('formateur_delete/<int:id>/',formateur_delete, name='formateur_delete'),
    
    
    
    

    path('stude/',Stud, name='stude'),
    path('add/',Add, name='add'),
    path('update/<int:id>/',update, name='update'),
    path('delete_student/<int:id>/', delete_student, name = 'delete_student'),
    
    
    # ################################ formations #############
    
    path('formations/',list_formations, name='list_formations'),
    path('add_formation/',add_formation, name='add_formation'),
    path('update_formation/<int:id>/',update_formation, name='update_formation'),
    path('delete_formation/<int:id>/',delete_formation, name='delete_formation'),
    
    
    
    ################################ incriptions #############
    
    
    
    path('liste_inscrie/',inscrie_list, name='liste_inscrie'),
    path('add_inscrie/',add_inscrie, name='add_inscrie'),
    path('edit_inscrie/<int:id>/',edit_inscrie, name='edit_inscrie'),
    path('delete_inscrie/<int:id>/',delete_inscrie, name='delete_inscrie'),
    path('generate_pdf/<int:inscrie_id>/', generate_pdf, name='generate_pdf'),
    
    
    
]