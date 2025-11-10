from django.core.management.base import BaseCommand
from usuario.notificacoes import GerenciadorNotificacoes
from django.utils import timezone

class Command(BaseCommand):
    help = 'Envia lembretes de treinos baseados no dia da semana'
    
    def handle(self, *args, **options):
        self.stdout.write(f"Verificando treinos para {timezone.now().strftime('%A, %d/%m/%Y')}...")
        
        GerenciadorNotificacoes.verificar_treinos_hoje()
        
        self.stdout.write(
            self.style.SUCCESS('Lembretes diários processados com sucesso!')
        )