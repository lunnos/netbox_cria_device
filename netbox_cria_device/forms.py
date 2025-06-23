from django import forms
from dcim.models import DeviceType, DeviceRole, Site, Region
from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField


class CustomDeviceForm(forms.Form):
    # O nome principal do dispositivo
    device_name = forms.CharField(
        label="Nome do Dispositivo",
        help_text="O identificador do dispositivo no inventário"
    )

    hostname = forms.CharField(
        label="Hostname (Campo Customizado)",
        widget=forms.TextInput(attrs={'readonly': True})
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        label="Site",
    )
    device_role = DynamicModelChoiceField(
        queryset=DeviceRole.objects.all(),
        label="Função do Dispositivo"
    )
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        label="Tipo de Dispositivo"
    )
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label="Tenant"
    )


class SiteModalForm(forms.Form):
    name = forms.CharField(
        label="Nome do Site"
    )
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label="Região"
    )
