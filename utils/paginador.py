from django.core.paginator import Paginator

def paginador_general(request,lista_model, page):
    try:
        paginador = Paginator(lista_model,page)
        paginador_model=paginador.page(page)
    except :
        paginador_model= paginador.page(1)
    return paginador_model