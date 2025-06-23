import json # Importa a biblioteca JSON
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify

from dcim.models import Device, Site
from .forms import CustomDeviceForm, SiteModalForm

# A função de gerar hostname não é mais necessária aqui, pois a lógica
# será movida para o JavaScript. Mantemos apenas como referência caso precise no futuro.
# def gerar_hostname_customizado(form_data): ...

class CustomDeviceAddView(View):
    template_name = 'netbox_cria_device/device_add_custom.html'

    def get(self, request):
        form = CustomDeviceForm()

        # Prepara os dados dos sites para o JavaScript
        # Criamos um dicionário mapeando o ID de cada site para o seu slug
        sites_map = {site.id: site.slug for site in Site.objects.all()}

        return render(request, self.template_name, {
            'form': form,
            'modal_form': SiteModalForm(),
            'sites_map_json': json.dumps(sites_map) # Converte o dicionário para uma string JSON
        })

    def post(self, request):
        form = CustomDeviceForm(request.POST)
        return_url = request.GET.get('return_url', '/dcim/devices/')

        if form.is_valid():
            device_name = form.cleaned_data['device_name']
            hostname = form.cleaned_data['hostname'] # Pega o hostname do campo do formulário

            # ATENÇÃO: Verifique se o nome do seu campo customizado é 'hostname'
            custom_fields_data = {
                'hostname': hostname
            }

            # Validação para garantir que o nome principal do dispositivo é único
            if Device.objects.filter(name__iexact=device_name).exists():
                 messages.error(request, f"Um dispositivo com o nome '{device_name}' já existe.")
                 return render(request, self.template_name, {'form': form, 'sites_map_json': self.get_sites_map_json()})

            novo_device = Device(
                name=device_name,
                device_type=form.cleaned_data['device_type'],
                device_role=form.cleaned_data['device_role'],
                site=form.cleaned_data['site'],
                tenant=form.cleaned_data['tenant'],
                status='planned',
                custom_fields=custom_fields_data
            )
            novo_device.full_clean()
            novo_device.save()

            messages.success(request, f"Dispositivo '{novo_device.name}' (Hostname: {hostname}) criado com sucesso!")
            return redirect(return_url)

        return render(request, self.template_name, {'form': form, 'sites_map_json': self.get_sites_map_json()})

    def get_sites_map_json(self):
        """Função auxiliar para evitar repetição de código."""
        sites_map = {site.id: site.slug for site in Site.objects.all()}
        return json.dumps(sites_map)

class SiteCreateModalView(View):
    def post(self, request):
        form = SiteModalForm(request.POST)
        if form.is_valid():
            try:
                new_site = Site(
                    name=form.cleaned_data['name'],
                    slug=slugify(form.cleaned_data['name']),
                    region=form.cleaned_data['region'],
                    status='active'
                )
                new_site.full_clean()
                new_site.save()

                return JsonResponse({
                    'status': 'success',
                    'id': new_site.id,
                    'text': str(new_site)
                })
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        return JsonResponse({'status': 'error', 'message': form.errors.as_json()}, status=400)