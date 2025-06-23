from extras.plugins import PluginTemplateExtension

class DeviceListButton(PluginTemplateExtension):
    model = 'dcim.device'

    def buttons(self):
        return self.render('netbox_cria_device/device_add_button.html')

template_extensions = [DeviceListButton]