from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )
    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def vercontato(request, contato_id):
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/vercontato.html', {
        'contato': contato,
        'id': contato_id
    })


def busca(request):
    termo = request.GET.get('termo')
    if termo is None or not termo:
        messages.add_message(request, messages.ERROR, 'Campo não pode ficar vazio!')
        return redirect('index')
    campos = Concat('nome', Value(' '), 'sobrenome')
    contatos = Contato.objects.annotate(
        nomecompleto=campos
    ).filter(
        Q(nomecompleto__icontains=termo) | Q(telefone__icontains=termo),
        mostrar=True
    ).order_by('-id')
    paginator = Paginator(contatos, 3)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
