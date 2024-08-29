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
                'nombre': f"{pedido.usuario.persona.nombre }  {pedido.usuario.persona.apellidos}",
                'codigo': pedido.numero_pedido,
                'cantidad_pedida': pedido.cantidad_pedida,
               
            }
        }
    )
