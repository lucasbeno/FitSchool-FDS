from django.utils import timezone
from django.contrib import messages
from .models import Notificacao, ConfirmacaoPresenca, Perfil, Treino, Frequencia
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class GerenciadorNotificacoes:
    
    @staticmethod
    def enviar_lembrete_treino(usuario, treino):
        """Envia lembrete para treino agendado"""
        try:
            perfil = Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            logger.warning(f"Perfil não encontrado para usuário {usuario.username}")
            return None
        
        if not perfil.notificacoes_ativadas:
            return None
        
        minutos_antes = perfil.lembrete_minutos_antes
        horario_treino = treino.data_hora
        horario_lembrete = horario_treino - timedelta(minutes=minutos_antes)
        
        if timezone.now() >= horario_lembrete:
            # Verifica se já foi enviada notificação recente para este treino
            notificacao_existente = Notificacao.objects.filter(
                usuario=usuario,
                treino_agendado=treino,
                tipo='lembrete_treino',
                data_criacao__date=timezone.now().date()
            ).exists()
            
            if not notificacao_existente:
                notificacao = Notificacao.objects.create(
                    usuario=usuario,
                    tipo='lembrete_treino',
                    titulo=f'Lembrete de Treino - {treino.tipo}',
                    mensagem=f'Seu treino de {treino.tipo} está agendado para {horario_treino.strftime("%H:%M")}. Não se esqueça!',
                    treino_agendado=treino,
                    data_envio=timezone.now()
                )
                
                # Atualiza último lembrete enviado
                perfil.ultimo_lembrete_enviado = timezone.now()
                perfil.save()
                
                logger.info(f"Lembrete enviado para {usuario.username} - Treino: {treino.tipo}")
                return notificacao
        
        return None
    
    @staticmethod
    def enviar_notificacao_sem_treino(usuario):
        """Envia notificação quando não há treinos agendados"""
        try:
            perfil = Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            return None
        
        if not perfil.notificacoes_ativadas:
            return None
        
        # Verifica se já foi enviada notificação hoje
        notificacao_existente = Notificacao.objects.filter(
            usuario=usuario,
            tipo='sem_treino',
            data_criacao__date=timezone.now().date()
        ).exists()
        
        if not notificacao_existente:
            notificacao = Notificacao.objects.create(
                usuario=usuario,
                tipo='sem_treino',
                titulo='Nenhum Treino Agendado',
                mensagem='Você não possui treinos agendados para hoje. Que tal agendar um?',
                data_envio=timezone.now()
            )
            
            logger.info(f"Notificação sem treino enviada para {usuario.username}")
            return notificacao
        
        return None
    
    @staticmethod
    def solicitar_confirmacao_presenca(usuario, treino):
        """Solicita confirmação de presença no treino"""
        # Verifica se já existe confirmação pendente
        notificacao_existente = Notificacao.objects.filter(
            usuario=usuario,
            treino_agendado=treino,
            tipo='confirmacao_presenca',
            lida=False
        ).exists()
        
        if not notificacao_existente:
            notificacao = Notificacao.objects.create(
                usuario=usuario,
                tipo='confirmacao_presenca',
                titulo='Confirmação de Presença',
                mensagem=f'Por favor, confirme sua presença no treino de {treino.tipo} agendado para {treino.data_hora.strftime("%H:%M")}.',
                treino_agendado=treino,
                data_envio=timezone.now()
            )
            
            logger.info(f"Solicitação de confirmação enviada para {usuario.username}")
            return notificacao
        
        return None
    
    @staticmethod
    def confirmar_presenca(usuario, treino):
        """Registra confirmação de presença"""
        confirmacao, created = ConfirmacaoPresenca.objects.get_or_create(
            usuario=usuario,
            treino=treino,
            defaults={'confirmado': True}
        )
        
        if not created:
            confirmacao.confirmado = True
            confirmacao.data_confirmacao = timezone.now()
            confirmacao.save()
        
        # Marca notificação como lida
        Notificacao.objects.filter(
            usuario=usuario,
            treino_agendado=treino,
            tipo='confirmacao_presenca',
            lida=False
        ).update(lida=True)
        
        # Atualiza frequência
        Frequencia.objects.update_or_create(
            usuario=usuario,
            data=timezone.now().date(),
            defaults={'status': 'PRESENTE'}
        )
        
        logger.info(f"Presença confirmada: {usuario.username} - Treino: {treino.tipo}")
        return confirmacao
    
    @staticmethod
    def verificar_treinos_agendados():
        """Verifica todos os treinos agendados e envia notificações"""
        agora = timezone.now()
        usuarios_com_notificacoes = Perfil.objects.filter(notificacoes_ativadas=True)
        
        for perfil in usuarios_com_notificacoes:
            usuario = perfil.user
            # Busca treinos do usuário para hoje com data/hora específica
            treinos_hoje = Treino.objects.filter(
                usuario=usuario,
                data_hora__date=agora.date(),
                data_hora__gt=agora,
                ativo=True
            )
            
            if treinos_hoje.exists():
                for treino in treinos_hoje:
                    GerenciadorNotificacoes.enviar_lembrete_treino(usuario, treino)
                    GerenciadorNotificacoes.solicitar_confirmacao_presenca(usuario, treino)
            else:
                GerenciadorNotificacoes.enviar_notificacao_sem_treino(usuario)