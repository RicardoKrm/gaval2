# cuentas/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# ... (tus clases CustomLoginView y CustomLogoutView) ...

# --- ¡AÑADE ESTA FUNCIÓN AL FINAL DEL ARCHIVO! ---
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