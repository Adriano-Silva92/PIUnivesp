# Importações de módulos do Django e Python nativo
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
from django.contrib import messages




class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html' # Template a ser renderizado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            # Se o usuário for superuser, vê todos os pedidos
            context['pedidos'] = Pedido.objects.all()
        else:
            # Se for usuários normais, veem apenas seus próprios pedidos
            context['pedidos'] = Pedido.objects.filter(usuario=self.request.user)

            # Busca pedidos atualizados com status Aprovado ou Negado que o usuário ainda não viu
            novos_status = Pedido.objects.filter(
                usuario=self.request.user,
                status__in=["Aprovado", "Negado"],
                visto_pelo_usuario=False
            )
            context['novos_pedidos_aprovados_ou_negados'] = novos_status

            # Marca esses pedidos como vistos
            for pedido in novos_status:
                pedido.visto_pelo_usuario = True
                pedido.save()
        # Todas as mensagens, ordenadas da mais recente para a mais antiga
        context['mensagens'] = Mensagem.objects.all().order_by('-data_criacao')
        # Apenas perfis com foto
        context['usuarios_com_foto'] = Profile.objects.exclude(foto='').select_related('user')

        # Identifica usuários logados com base nas sessões ativas para mostrar no painel
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        for session in sessions: #Faz a varredura nas sessões
            data = session.get_decoded()
            uid = data.get('_auth_user_id')
            if uid:
                uid_list.append(uid)

        usuarios_logados = User.objects.filter(id__in=uid_list)
        context['usuarios_logados'] = Profile.objects.filter(user__in=usuarios_logados).select_related('user')

        context['user'] = self.request.user # Adiciona usuário atual ao contexto

        # Conta quantos pedidos existem por status para o gráfico
        status_counts = Pedido.objects.values('status').annotate(total=Count('id'))
        context['grafico_dados'] = {item['status']: item['total'] for item in status_counts}
        context['count_aprovado'] = context['grafico_dados'].get('Aprovado', 0)
        context['count_negado'] = context['grafico_dados'].get('Negado', 0)
        context['count_pendente'] = context['grafico_dados'].get('Pendente', 0)

        return context

    # Quando um formulário for submetido (ex: mensagem no chat)
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
def apagar_mensagem(request, mensagem_id): #Função para apagar mensagem
    mensagem = get_object_or_404(Mensagem, id=mensagem_id)
    if mensagem.usuario == request.user: #Verifica se a mensagem é do próprio usuário
        mensagem.delete() # Se for ele tem permissão de apagar
        return redirect('index')
    else: # Se não, ele recebe uma mensagem de erro
        return HttpResponseForbidden("Você não tem permissão para apagar esta mensagem.")

#CRIAR PEDIDO COM E-MAIL
@require_POST
@login_required
def criar_pedido(request): #Definindo uma função para criar pedidos
    #Abaixo são itens que devem ser preenchidos no formulário
    produto = request.POST.get('produto', '').upper()
    quantidade = request.POST.get('quantidade')
    tipo = request.POST.get('tipo')
    prioridade = request.POST.get('prioridade')
    foto = request.FILES.get('foto')

    if produto and quantidade and tipo and prioridade: #Verifica se todos os campos foram preenchidos
        pedido = Pedido.objects.create( #Enquanto todos os campos não forem preenchidos corretamente o novo pedido não é criado
            usuario=request.user,
            produto=produto,
            quantidade=quantidade,
            tipo=tipo,
            prioridade=prioridade,
            status="Pendente",
            foto=foto
        )
        #Quando um pedido é criado dispara um E-mail
        # === CONTEXTO DO E-MAIL PARA NOVO PEDIDO CRIADO===
        contexto = {
            'usuario': request.user.get_full_name() or request.user.username,
            'produto': pedido.produto,
            'tipo': pedido.tipo,
            'prioridade': pedido.prioridade,
            'status': pedido.status,
            'data': datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
            'cor_fundo': '#ffc107',  # Laranja para pendente
            'icone': '✅',
            'mensagem': 'Pedido Cadastrado com Sucesso!',
            'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ser ajustado para link direto posteriormente
            'botao': 'Ver Pedido',
        }

        html_content = render_to_string('emails/pedido_email.html', contexto) #Renderiza o template pedido_email.html com dados do contexto
        text_content = strip_tags(html_content)

        # === DESTINATÁRIOS DO E-MAIL=== ADM E USUARIO QUE FEZ O PEDIDO
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
        # Adiciona a mensagem de sucesso para o usuário
        messages.success(request, f"O PEDIDO '{pedido.produto}' FOI CRIADO COM SUCESSO!")

    return redirect('index')

#TESTANDO NOVO USUARIO LOGADO COM MIDDLEWARE
@login_required
def usuarios_logados_partial(request): #Definindo uma função para exibir usuários logados em tempo real
    limite = timezone.now() - timedelta(seconds=10)  # Atualiza usuários logados a cada 10s
    usuarios_logados = Profile.objects.filter(last_seen__gte=limite).select_related('user') #Faz a captura deste usuário que está logado
    return render(request, 'partials/usuarios_logados.html', {'usuarios_logados': usuarios_logados}) #Renderiza o template uruarios_logados.html

#APROVAR PEDIDO COM E-MAIL
@login_required
@require_POST
def aprovar_pedido(request, pedido_id): # Definindo uma função para aprovar pedidos
    if not request.user.is_superuser: #Verifica se o usuário não é um super user através do not user (Somente superuser aprova ou nega pedidos)
        return HttpResponseForbidden("Você não tem permissão para aprovar pedidos.")

    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "Aprovado" #Caso o superuser Aprova o status passa para Aprovado
    pedido.visto_pelo_usuario = False
    pedido.save()

    #Se Aprovado Dispara o E-mail abaixo
    # === CONTEXTO DO E-MAIL PARA APROVADO===
    contexto = {
        'usuario': pedido.usuario.get_full_name() or pedido.usuario.username,
        'produto': pedido.produto,
        'tipo': pedido.tipo,
        'prioridade': pedido.prioridade,
        'status': pedido.status,
        'data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'cor_fundo': '#28a745',  # Verde para aprovado
        'icone': '✅',
        'mensagem': f'O Pedido #{ pedido.id } foi Aprovado com Sucesso',
        'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ajustar depois
    }

    html_content = render_to_string('emails/pedido_email.html', contexto) #Renderiza o template pedido_email.html com o contexto acima
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

    return redirect('/?status_msg=PEDIDO+%s+FOI+APROVADO' % pedido.produto) #Exibe um Alert personalizado na tela

#NEGAR PEDIDO COM E-MAIL
@login_required
@require_POST
def negar_pedido(request, pedido_id): #Definindo uma função para Negar Pedidos
    if not request.user.is_superuser: #Novamente verifica se realmente é um super user
       return HttpResponseForbidden("Você não tem permissão para negar pedidos.")
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "Negado" #O status muda para Negado
    pedido.visto_pelo_usuario = False
    pedido.save()

    #Toda vez que um pedido é Negado dispara um E-mail
    # === CONTEXTO DO E-MAIL PARA NEGADO===
    contexto = {
        'usuario': pedido.usuario.get_full_name() or pedido.usuario.username,
        'produto': pedido.produto,
        'tipo': pedido.tipo,
        'prioridade': pedido.prioridade,
        'status': pedido.status,
        'data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'cor_fundo': '#dc3545',  # Vermelho para negado
        'icone': '❌',
        'mensagem': f'O Pedido #{ pedido.id } foi Negado',
        'link_pedido': 'https://www.grupotechnik.com.br/',  # Pode ajustar depois
    }

    html_content = render_to_string('emails/pedido_email.html', contexto) #Renderiza o template pedido_email.html com o contexto acima
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

    return redirect('/?status_msg=PEDIDO+%s+FOI+NEGADO' % pedido.produto) #Exibe um Alert personalizado Peidido Negado

#TESTANDO VIEW PARA APAGAR PEDIDO
@login_required
@require_POST
def excluir_pedido(request, pedido_id):
    if not request.user.is_superuser:  # Verifica se o usuário é superuser
        return HttpResponseForbidden("Você não tem permissão para excluir pedidos.")

    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = "EXCLUÍDO"  # Marcar como excluído ou removido
    pedido.delete()

    # Contexto do e-mail para exclusão
    contexto = {
        'usuario': pedido.usuario.get_full_name() or pedido.usuario.username,
        'produto': pedido.produto,
        'tipo': pedido.tipo,
        'prioridade': pedido.prioridade,
        'status': pedido.status,
        'data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'cor_fundo': '#dc3545',  # Vermelho para excluído
        'icone': '❌',
        'mensagem': f'O Pedido Abaixo Foi Excluído',
        'link_pedido': 'https://www.grupotechnik.com.br/',  # Ajuste se necessário
    }

    html_content = render_to_string('emails/pedido_email.html', contexto)  # Renderiza o template com o contexto
    text_content = strip_tags(html_content)

    # Destinatários - Admin e Usuário que fez o pedido
    superusers = User.objects.filter(is_superuser=True).values_list('email', flat=True)
    destinatarios = list(superusers) + [pedido.usuario.email]

    email = EmailMultiAlternatives(
        subject='🔰 Pedido Excluído❌ - Sistema de Compras - ⚠️ Não Responder ❌',
        body=text_content,
        from_email='adriano.josias.silva.199@gmail.com',
        to=destinatarios,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


    return redirect('/?status_msg=PEDIDO+%s+FOI+EXCLUIDO' % pedido.produto) #Exibe um Alert personalizado Peidido Negado

#Para checar se status se status foi visto pelo usuario -> se não return Alert
@login_required
def checar_status_pedidos(request): #Definindo uma função para checar se algum status foi alterado
    pedidos = Pedido.objects.filter(usuario=request.user, visto_pelo_usuario=False)
    response_data = []

    for pedido in pedidos: #Faz a varredura nos produtos e status
        response_data.append({
            'produto': pedido.produto,
            'status': pedido.status
        })
        pedido.visto_pelo_usuario = True #Encontrado algum pedido modificado
        pedido.save()

    return JsonResponse({'novos_status': response_data}) #É exibido o Alert personalizado Status Alterado

# Exportar PDF
@login_required
def exportar_pedidos_pdf(request): #Definindo uma função para exportar PDF
    if request.user.is_superuser: #Se é um super usuário
        pedidos = Pedido.objects.all() #Consegue exportar todos os pedidos
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)#Se usuário comum, somente seus próprios pedidos

    html_string = render_to_string('relatorios/pedidos_pdf.html', {'pedidos': pedidos}) #Renderiza o template pedidos_pdf.html
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    data_atual = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M') #Coletando a Data e Hora Atual da Exportação
    nome_arquivo = f"relatorio_pedidos_{data_atual}.pdf" #Define o nome do arquivo como relatorio_pedidos+(data e hora).pdf

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    return response

# Exportar CSV
@login_required
def exportar_pedidos_csv(request): #Definindo uma função para Exportar CSV
    if request.user.is_superuser: #Novamente verifica se é um superuser
        pedidos = Pedido.objects.all() #Se sim, exporta todos os pedidos
    else:
        pedidos = Pedido.objects.filter(usuario=request.user) #Se usuário comum, exporta seus pedidos

    data_atual = datetime.datetime.now().strftime('%d-%m-%Y_%Hh%Mm') #Coleta a data e hora atual da exportação
    nome_arquivo = f"relatorio_pedidos_{data_atual}.csv" #Define o nome do arquivo relatório_pedidos+(data e hora).csv

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    # Adiciona a formatação para que o Excel reconheça UTF-8
    response.write('\ufeff'.encode('utf8'))

    #DADOS DA EXPORTAÇÃO CSV
    writer = csv.writer(response)
    #Escrevendo as colunas do arquivo
    writer.writerow(['ID','USUÁRIO', 'PRODUTO', 'QUANTIDADE', 'TIPO', 'PRIORIDADE', 'STATUS', 'DATA'])

    for pedido in pedidos: #Faz a varredura em todos os dados da tabela de pedidos
        writer.writerow([
            pedido.id,
            pedido.usuario.username,
            pedido.produto,
            pedido.quantidade,
            pedido.tipo,
            pedido.prioridade,
            pedido.status,
            pedido.data.strftime('%d/%m/%Y')
        ])

    return response

