from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Treino
import datetime


DIAS_DA_SEMANA = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

@shared_task
def enviar_lembretes_de_treino():
    """
    Tarefa agendada para rodar todos os dias às 00:01.
    Envia e-mails de lembrete para usuários com treinos agendados 
    para o dia e que tenham as notificações ativadas.
    """

    hoje_index = datetime.date.today().weekday() 
    hoje_nome = DIAS_DA_SEMANA.get(hoje_index)

    if not hoje_nome:
        return "Dia inválido (não mapeado no DIAS_DA_SEMANA)."

    usuarios_para_notificar = User.objects.filter(
        atleta__notificacoes_email=True
    ).exclude(email__exact='')

    print(f"Rodando lembretes para {hoje_nome}. Usuários a notificar: {usuarios_para_notificar.count()}")

    for user in usuarios_para_notificar:
        
        treinos_de_hoje = Treino.objects.filter(
            usuario=user, 
            dia_semana=hoje_nome
        )

        if treinos_de_hoje.exists():
            
            lista_nomes_treinos = [t.nome for t in treinos_de_hoje]
            
            # Monta o e-mail
            assunto = f"Lembrete FitSchool: Hoje é dia de {', '.join(lista_nomes_treinos)}!"
            
            corpo = (
                f"Olá, {user.username}!\n\n"
                f"Este é um lembrete automático de que hoje ({hoje_nome}) é dia do(s) seu(s) treino(s):\n\n"
            )
            for treino in treinos_de_hoje:
                corpo += f"- {treino.nome}\n"
            
            corpo += "\nBom treino!\n\n- Equipe FitSchool"

            try:
                send_mail(
                    assunto,
                    corpo,
                    'nao-responda@fitschool.com', 
                    [user.email],                  
                    fail_silently=False,
                )
                print(f"E-mail enviado com sucesso para {user.email}")
            except Exception as e:
                print(f"FALHA ao enviar e-mail para {user.email}: {e}")

    return f"Tarefa de lembretes concluída para o dia {hoje_nome}."