from netbox.plugins import PluginConfig

class NetboxCriaDevicePluginConfig(PluginConfig):
    name = 'netbox_cria_device'
    verbose_name = 'Criação de Dispositivos'
    description = 'Adiciona um botão para criação de dispositivos.'
    version = '1.0'
    author = 'Luan'
    base_url = 'cria-device'
    required_settings = []
    default_settings = {}

config = NetboxCriaDevicePluginConfig