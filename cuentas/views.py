# cuentas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# cuentas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction, connection

# Asumiremos que los decoradores se moverán o importarán desde su nueva ubicación.
from flota.decorators import es_supervisor_o_admin
from .forms import UsuarioCreacionForm, UsuarioEdicionForm


@login_required
def perfil_view(request):
    """
    Muestra la página de perfil del usuario que ha iniciado sesión.
    """
    context = {
        'user': request.user
    }
    # Le decimos a Django que busque el template en 'cuentas/perfil.html'
    return render(request, 'cuentas/perfil.html', context)


@login_required
@user_passes_test(es_supervisor_o_admin) # Solo supervisores y admins pueden ver la lista
def lista_usuarios(request):
    """
    Muestra una lista de todos los usuarios del tenant actual.
    """
    connection.set_tenant(request.tenant)

    # Obtenemos todos los usuarios, excepto el superusuario si existiera en este tenant (poco probable pero seguro)
    # y los ordenamos por nombre de usuario.
    usuarios = User.objects.filter(is_superuser=False).order_by('username')

    context = {
        'usuarios': usuarios
    }
    return render(request, 'cuentas/administracion/lista_usuarios.html', context) # Actualizaremos la ruta de la plantilla


@login_required
@user_passes_test(es_supervisor_o_admin) # Solo supervisores y admins pueden crear usuarios
def crear_usuario(request):
    """
    Gestiona la creación de un nuevo usuario y su asignación a un grupo (rol).
    """
    connection.set_tenant(request.tenant)

    if request.method == 'POST':
        form = UsuarioCreacionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Obtenemos los datos limpios del formulario
                    username = form.cleaned_data['username']
                    password = form.cleaned_data['password']
                    email = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    grupo = form.cleaned_data['grupo']

                    # Creamos el nuevo usuario
                    nuevo_usuario = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )

                    # Asignamos el usuario al grupo seleccionado
                    nuevo_usuario.groups.add(grupo)

                    messages.success(request, f'Usuario "{username}" creado y asignado al rol "{grupo.name}" con éxito.')
                    return redirect('lista_usuarios') # Asumimos que el nombre de la URL no cambia

            except Exception as e:
                messages.error(request, f'Ocurrió un error al crear el usuario: {e}')

    else: # Si es una petición GET
        form = UsuarioCreacionForm()

    context = {
        'form': form
    }
    return render(request, 'cuentas/administracion/crear_usuario.html', context) # Actualizaremos la ruta


@login_required
@user_passes_test(es_supervisor_o_admin) # Solo supervisores y admins pueden editar
def editar_usuario(request, user_id):
    """
    Gestiona la edición de los datos y el rol de un usuario existente.
    """
    connection.set_tenant(request.tenant)
    usuario_a_editar = get_object_or_404(User, pk=user_id, is_superuser=False)

    if request.method == 'POST':
        form = UsuarioEdicionForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Actualizamos los datos del usuario
                    usuario_a_editar.first_name = form.cleaned_data['first_name']
                    usuario_a_editar.last_name = form.cleaned_data['last_name']
                    usuario_a_editar.email = form.cleaned_data['email']
                    usuario_a_editar.save()

                    # Actualizamos el grupo (rol)
                    grupo_nuevo = form.cleaned_data['grupo']
                    usuario_a_editar.groups.clear() # Quitamos todos los grupos anteriores
                    usuario_a_editar.groups.add(grupo_nuevo) # Añadimos el nuevo grupo

                    messages.success(request, f'Usuario "{usuario_a_editar.username}" actualizado con éxito.')
                    return redirect('lista_usuarios') # Asumimos que el nombre de la URL no cambia

            except Exception as e:
                messages.error(request, f'Ocurrió un error al editar el usuario: {e}')

    else: # Si es una petición GET
        # Pre-poblamos el formulario con los datos actuales del usuario
        initial_data = {
            'first_name': usuario_a_editar.first_name,
            'last_name': usuario_a_editar.last_name,
            'email': usuario_a_editar.email,
            'grupo': usuario_a_editar.groups.first(), # Obtenemos el primer (y único) grupo del usuario
        }
        form = UsuarioEdicionForm(initial=initial_data)

    context = {
        'form': form,
        'usuario_a_editar': usuario_a_editar
    }
    return render(request, 'cuentas/administracion/editar_usuario.html', context) # Actualizaremos la ruta