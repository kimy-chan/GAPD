# pedidos/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def enviar_notificacion_pedido(pedido):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notificaciones',
        {
            'type': 'enviar_pedido',
            'pedido': {
                'nombre': pedido.usuario.persona.nombre,
                #'codigo': pedido.codigo,
                'cantidad_pedida': pedido.cantidad_pedida,
               
            }
        }
    )
