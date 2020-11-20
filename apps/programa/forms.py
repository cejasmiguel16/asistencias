from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput
from datetime import date

from .models import Programa, AsignacionBeneficio

class AsignacionBeneficioForm(forms.ModelForm):
    class Meta:
        model = AsignacionBeneficio
        fields = '__all__'
        widgets = {
            'fecha_entrega': DateInput(format='%y-%m-%d', attrs={'type': 'date'})
        }

    #Verificar que la fecha de asignación de un beneficio no sea posterior a la fecha actual.
    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data['fecha_entrega']
        if fecha_entrega > date.today():
            raise ValidationError('No se puede asignar una fecha posterior a la fecha ACTUAL')
        return fecha_entrega

    #Verificar que la cantidad del beneficio no sea menor a 1.
    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 1 :
            raise ValidationError('No se puede asignar una cantidad menor a 1')
        return cantidad


class FiltrarAsignacionesForm(forms.Form):
    programas = Programa.objects.all()
    programa = forms.ModelChoiceField(queryset=programas)


class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ('nombre', 'tipo_asistencias', 'requisitos', 'fecha_inicio', 'fecha_fin')

        widgets = {
            'requisitos': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin': DateInput(format='%y-%m-%d', attrs={'type': 'date'})
        }

    def clean_requisitos(self):
        requisitos = self.cleaned_data['requisitos']
        if requisitos:
            extension = requisitos.name.rsplit('.', 1)[1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
        return requisitos

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = self.cleaned_data['fecha_inicio']
        fecha_fin = self.cleaned_data['fecha_fin']
        # Verifica que la fecha de inicio sea anterior a fecha fin.
        if fecha_fin and fecha_inicio > fecha_fin:
            raise ValidationError(
                {'fecha_inicio': 'La Fecha de Inicio no puede ser posterior que la fecha fin'},
                code='invalido'
            )
        return cleaned_data
