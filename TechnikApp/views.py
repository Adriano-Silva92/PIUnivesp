from django.views.generic import TemplateView
from .models import Pedido, Mensagem, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
import datetime
import csv
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta




class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            context['pedidos'] = Pedido.objects.all()
        else:
            context['pedidos'] = Pedido.objects.filter(usuario=self.request.user)

            # Buscar pedidos atualizados (aprovados ou negados) ainda não vistos pelo usuário
            novos_status = Pedido.objects.filter(
                usuario=self.request.user,
                status__in=["Aprovado", "Negado"],
                visto_pelo_usuario=False
            )
            context['novos_pedidos_aprovados_ou_negados'] = novos_status

            # Marcar como vistos pelo usuário -> Isso é para alerts!
            for pedido in novos_status:
                pedido.visto_pelo_usuario = True
                pedido.save()

        context['mensagens'] = Mensagem.objects.all().order_by('-data_criacao')
        context['usuarios_com_foto'] = Profile.objects.exclude(foto='').select_related('user')

        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        for session in sessions:
            data = session.get_decoded()
            uid = data.get('_auth_user_id')
            if uid:
                uid_list.append(uid)

        usuarios_logados = User.objects.filter(id__in=uid_list)
        context['usuarios_logados'] = Profile.objects.filter(user__in=usuarios_logados).select_related('user')

        context['user'] = self.request.user

        status_counts = Pedido.objects.values('status').annotate(total=Count('id'))
        context['grafico_dados'] = {item['status']: item['total'] for item in status_counts}
        context['count_aprovado'] = context['grafico_dados'].get('Aprovado', 0)
        context['count_negado'] = context['grafico_dados'].get('Negado', 0)
        context['count_pendente'] = context['grafico_dados'].get('Pendente', 0)

        return context

    def post(self, request, *args, **kwargs):
        mensagem = request.POST.get('mensagem')
        if mensagem:
            Mensagem.objects.create(
                usuario=request.user,
                texto=mensagem,
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('/?mensagem_enviada=true')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False}, status=400)
        return redirect('index')


@require_POST
@login_required
def apagar_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    if mensagem.usuario == request.user:
        mensagem.delete()
        return redirect('index')
    else:
        return HttpResponseForbidden("Você não tem permissão para apagar esta mensagem.")

#CRIAR PEDIDO COM E-MAIL
@require_POST
@login_required
def criar_pedido(request):
    produto = request.POST.get('produto')
    quantidade = request.POST.get('quantidade')
    setor = request.POST.get('setor')
    prioridade = request.POST.get('prioridade')

    if produto and quantidade and setor and prioridade:
        pedido = Pedido.objects.create(
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            setor=setor,
            prioridade=prioridade,
            status="Pendente"
        )

        # === CONTEXTO DO E-MAIL ===
        contexto = {
            'usuario': request.user.get_full_name() or request.user.username,
            'produto': pedido.produto,
            'setor': pedido.setor,
            'prioridade': pedido.prioridade,
            'status': pedido.status,
            'data': datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
            'cor_fundo': '#ffc107',  # Laranja para pendente
            'icone': '✅',
            'mensagem': 'Pedido Cadastrado com Sucesso!',
            'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ser ajustado para link direto posteriormente
            'botao': 'Ver Pedido',
        }

        html_content = render_to_string('emails/pedido_email.html', contexto)
        text_content = strip_tags(html_content)

        # === DESTINATÁRIOS === ADM E USUARIO QUE FEZ O PEDIDO
        superusers = User.objects.filter(is_superuser=True).values_list('email', flat=True)
        destinatarios = list(superusers) + [request.user.email]

        email = EmailMultiAlternatives(
            subject='🔰 Novo Pedido Cadastrado✅ - Sistema de Compras- ⚠️ Não Responder ❌',
            body=text_content,
            from_email='adriano.josias.silva.199@gmail.com',
            to=destinatarios,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    return redirect('index')

#TESTANDO NOVO USUARIO LOGADO COM MIDDLEWARE
@login_required
def usuarios_logados_partial(request):
    limite = timezone.now() - timedelta(seconds=10)  # ajuste o tempo se quiser
    usuarios_logados = Profile.objects.filter(last_seen__gte=limite).select_related('user')
    return render(request, 'partials/usuarios_logados.html', {'usuarios_logados': usuarios_logados})

#APROVAR PEDIDO COM E-MAIL
@login_required
@require_POST
def aprovar_pedido(request, pedido_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para aprovar pedidos.")

    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "Aprovado"
    pedido.visto_pelo_usuario = False
    pedido.save()

    # === CONTEXTO DO E-MAIL ===
    contexto = {
        'usuario': pedido.usuario.get_full_name() or pedido.usuario.username,
        'produto': pedido.produto,
        'setor': pedido.setor,
        'prioridade': pedido.prioridade,
        'status': pedido.status,
        'data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'cor_fundo': '#28a745',  # Verde para aprovado
        'icone': '✅',
        'mensagem': f'O Pedido #{ pedido.id } foi Aprovado com Sucesso',
        'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ajustar depois
    }

    html_content = render_to_string('emails/pedido_email.html', contexto)
    text_content = strip_tags(html_content)

    # === DESTINATÁRIOS === ADM E USUARIO QUE FEZ O PEDIDO
    superusers = User.objects.filter(is_superuser=True).values_list('email', flat=True)
    destinatarios = list(superusers) + [pedido.usuario.email]

    email = EmailMultiAlternatives(
        subject='🔰 Novo Pedido Aprovado✅ - Sistema de Compras- ⚠️ Não Responder ❌',
        body=text_content,
        from_email='adriano.josias.silva.199@gmail.com',
        to=destinatarios,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('/?status_msg=Pedido+%s+foi+aprovado' % pedido.produto)

#NEGAR PEDIDO COM E-MAIL
@login_required
@require_POST
def negar_pedido(request, pedido_id):
    if not request.user.is_superuser:
       return HttpResponseForbidden("Você não tem permissão para negar pedidos.")
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "Negado"
    pedido.visto_pelo_usuario = False
    pedido.save()

    # === CONTEXTO DO E-MAIL ===
    contexto = {
        'usuario': pedido.usuario.get_full_name() or pedido.usuario.username,
        'produto': pedido.produto,
        'setor': pedido.setor,
        'prioridade': pedido.prioridade,
        'status': pedido.status,
        'data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'cor_fundo': '#dc3545',  # Vermelho para negado
        'icone': '❌',
        'mensagem': f'O Pedido #{ pedido.id } foi Negado',
        'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ajustar depois
    }

    html_content = render_to_string('emails/pedido_email.html', contexto)
    text_content = strip_tags(html_content)

    # === DESTINATÁRIOS === ADM E USUARIO QUE FEZ O PEDIDO
    superusers = User.objects.filter(is_superuser=True).values_list('email', flat=True)
    destinatarios = list(superusers) + [pedido.usuario.email]

    email = EmailMultiAlternatives(
        subject='🔰 Novo Pedido Negado❌  - Sistema de Compras- ⚠️ Não Responder ❌',
        body=text_content,
        from_email='adriano.josias.silva.199@gmail.com',
        to=destinatarios,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('/?status_msg=Pedido+%s+foi+negado' % pedido.produto)

#Para checar se status se status foi visto pelo usuario -> se não return Alert
@login_required
def checar_status_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user, visto_pelo_usuario=False)
    response_data = []

    for pedido in pedidos:
        response_data.append({
            'produto': pedido.produto,
            'status': pedido.status
        })
        pedido.visto_pelo_usuario = True
        pedido.save()

    return JsonResponse({'novos_status': response_data})

# Exportar PDF
@login_required
def exportar_pedidos_pdf(request):
    if request.user.is_superuser:
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)

    html_string = render_to_string('relatorios/pedidos_pdf.html', {'pedidos': pedidos})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    data_atual = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')
    nome_arquivo = f"relatorio_pedidos_{data_atual}.pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    return response

# Exportar CSV
@login_required
def exportar_pedidos_csv(request):
    if request.user.is_superuser:
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)

    data_atual = datetime.datetime.now().strftime('%d-%m-%Y_%Hh%Mm')
    nome_arquivo = f"relatorio_pedidos_{data_atual}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    # Adiciona a formatção para que o Excel reconheça UTF-8
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['ID','USUÁRIO', 'PRODUTO', 'QUANTIDADE', 'SETOR', 'PRIORIDADE', 'STATUS', 'DATA'])

    for pedido in pedidos:
        writer.writerow([
            pedido.id,
            pedido.usuario.username,
            pedido.produto,
            pedido.quantidade,
            pedido.setor,
            pedido.prioridade,
            pedido.status,
            pedido.data.strftime('%d/%m/%Y')
        ])

    return response

