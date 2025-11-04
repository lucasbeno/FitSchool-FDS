from django.core.management.base import BaseCommand
from django.utils import timezone
from usuario.models import Usuario, Treino
from usuario.notificacoes import GerenciadorNotificacoes
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Envia lembretes de treinos agendados'
    
    def handle(self, *args, **options):
        agora = timezone.now()
        usuarios = Usuario.objects.filter(notificacoes_ativadas=True)
        
        for usuario in usuarios:
            treinos_hoje = Treino.objects.filter(
                usuario=usuario,
                data_hora__date=agora.date(),
                data_hora__gt=agora
            )
            
            if treinos_hoje.exists():
                for treino in treinos_hoje:
                    GerenciadorNotificacoes.enviar_lembrete_treino(usuario, treino)
                    GerenciadorNotificacoes.solicitar_confirmacao_presenca(usuario, treino)
            else:
                GerenciadorNotificacoes.enviar_notificacao_sem_treino(usuario)
        
        self.stdout.write(
            self.style.SUCCESS(f'Lembretes processados em {agora}')
        )