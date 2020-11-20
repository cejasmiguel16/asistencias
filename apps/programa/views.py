from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import ProgramaForm, AsignacionBeneficioForm, FiltrarAsignacionesForm
from .models import Programa, AsignacionBeneficio


def programa_lista(request):
    programas = Programa.objects.all()
    return render(request, 'programa/lista.html',
                  {'programas': programas})


def programa_detalle(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    return render(request,
                  'programa/detalle.html',
                  {'programa': programa})


def programa_create(request):
    nuevo_programa = None
    if request.method == 'POST':
        programa_form = ProgramaForm(request.POST, request.FILES)
        if programa_form.is_valid():
            # Se guardan los datos que provienen del formulario en la B.D.
            nuevo_programa = programa_form.save(commit=True)
            messages.success(request,
                             'Se ha agregado correctamente el Programa {}'.format(nuevo_programa))
            return redirect(reverse('programa:programa_detalle', args={nuevo_programa.id}))
    else:
        programa_form = ProgramaForm()

    return render(request, 'programa/programa_form.html',
                  {'form': programa_form})


def programa_delete(request):
    if request.method == 'POST':
        if 'id_programa' in request.POST:
            programa = get_object_or_404(Programa, pk=request.POST['id_programa'])
            nombre_programa = programa.nombre
            programa.delete()
            messages.success(request, 'Se ha eliminado exitosamente el Programa {}'.format(nombre_programa))
        else:
            messages.error(request, 'Debe indicar qué Programa se desea eliminar')
    return redirect(reverse('programa:programa_lista'))


def programa_edit(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    if request.method == 'POST':
        form_programa = ProgramaForm(request.POST, request.FILES, instance=programa)
        if form_programa.is_valid():
            form_programa.save()
            messages.success(request, 'Se ha actualizado correctamente el Programa')
            return redirect(reverse('programa:programa_detalle', args=[programa.id]))
    else:
        form_programa = ProgramaForm(instance=programa)

    return render(request, 'programa/programa_edit.html', {'form': form_programa})


def NuevaAsignacionBeneficio(request):
    data = {
        "form" : AsignacionBeneficioForm()
    }
    if request.method == 'POST':
        formulario = AsignacionBeneficioForm(request.POST)
        if formulario.is_valid():
            #Verificar que no se asigne en la misma fecha, mas de un beneficio a una misma persona.
            f= formulario.save(commit=False)
            persona = f.persona
            fecha = f.fecha_entrega
            #EN ESTE PUNTO SE CONTROLA QUE UNA PERSONA NO PUEDA RECIBIR 2 ASIGNACIONES LA MISMA FECHA
            asignaciones = AsignacionBeneficio.objects.filter(persona=persona)
            for a in asignaciones:
                if fecha == a.fecha_entrega:
                    messages.error(request, 'No se puede asignar mas de un beneficio la misma fecha')
                    return redirect(to='programa:programa_lista')
            f.save()
            messages.success(request, 'Se agrego una nueva asignacion')
            return redirect(to='programa:programa_lista')
        data["form"] = formulario

    return render(request, 'programa/asignacion_beneficio_form.html', data)


""" Generar una vista y templates para mostrar un listado de los beneficios asignados para un Programa y
rango de fechas en particular. """

def ListarAsignaciones(request):
    #asignaciones es la variable a la cual se van a aplicar los filtros en caso de ser necesario
    asignaciones = AsignacionBeneficio.objects.all()
    data = {
        "form" : FiltrarAsignacionesForm(),
        "asignaciones" : asignaciones
    }
    #SI EL FILTRO MANDA UN REQUEST POST ENTRA POR EL SIGUIENTE IF
    if request.method == 'POST':
        programa = request.POST.get('programa')
        """ Generar una vista y templates para mostrar un listado de los beneficios asignados para un Programa y
        rango de fechas en particular """
        if AsignacionBeneficio.objects.filter(programa=programa).exists():
            #Si encuentra una asignacion que este relacionada con el programa que se indico en el filtro
            #se aplica filtro a la variable asignaciones creada anteriormente
            asignaciones = asignaciones.filter(programa=programa)
            data["asignaciones"] = asignaciones
            return render(request, 'programa/listado_asignaciones.html', data)

    return render(request, 'programa/listado_asignaciones.html', data)
