from django.shortcuts import render, get_object_or_404
from .models import Contato
from django.core.paginator import Paginator


def index(request):
    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def vercontato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    return render(request, 'contatos/vercontato.html', {
        'contato': contato
    })
