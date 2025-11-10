from django.utils import timezone
from django.contrib import messages
from .models import Notificacao, ConfirmacaoPresenca, Perfil, Treino, Frequencia
from datetime import timedelta, datetime
import logging

logger = logging.getLogger(__name__)

class GerenciadorNotificacoes:
    
    @staticmethod
    def enviar_lembrete_treino(usuario, treino):
        """Envia lembrete para treino baseado no dia da semana"""
        try:
            perfil = Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            logger.warning(f"Perfil não encontrado para usuário {usuario.username}")
            return None
        
        if not perfil.notificacoes_ativadas:
            return None
        
        dia_hoje = timezone.now().strftime('%A').lower()
        dias_semana = {
            'sunday': 'domingo',
            'monday': 'segunda',
            'tuesday': 'terça', 
            'wednesday': 'quarta',
            'thursday': 'quinta',
            'friday': 'sexta',
            'saturday': 'sábado'
        }
        
        dia_treino = treino.dia_semana.lower()
        dia_hoje_ptbr = dias_semana.get(dia_hoje, '')
        
        if dia_treino != dia_hoje_ptbr:
            return None 
        
        minutos_antes = perfil.lembrete_minutos_antes
        horario_lembrete = timezone.now() + timedelta(minutes=minutos_antes)
        
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
                titulo=f' Lembrete de Treino - {treino.tipo}',
                mensagem=f'Hoje é seu treino de {treino.tipo} ({treino.dia_semana}). Horário sugerido: {horario_lembrete.strftime("%H:%M")}. Não se esqueça!',
                treino_agendado=treino,
                data_envio=timezone.now()
            )
            
            perfil.ultimo_lembrete_enviado = timezone.now()
            perfil.save()
            
            logger.info(f"Lembrete enviado para {usuario.username} - Treino: {treino.tipo} - Dia: {treino.dia_semana}")
            return notificacao
        
        return None
    
    @staticmethod
    def enviar_notificacao_sem_treino(usuario):
        """Envia notificação quando não há treinos agendados para hoje"""
        try:
            perfil = Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            return None
        
        if not perfil.notificacoes_ativadas:
            return None
        
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
        """Solicita confirmação de presença no treino do dia"""
        notificacao_existente = Notificacao.objects.filter(
            usuario=usuario,
            treino_agendado=treino,
            tipo='confirmacao_presenca',
            lida=False,
            data_criacao__date=timezone.now().date()
        ).exists()
        
        if not notificacao_existente:
            notificacao = Notificacao.objects.create(
                usuario=usuario,
                tipo='confirmacao_presenca',
                titulo='✅ Confirmação de Presença',
                mensagem=f'Por favor, confirme sua presença no treino de {treino.tipo} de hoje ({treino.dia_semana}).',
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
        
        Notificacao.objects.filter(
            usuario=usuario,
            treino_agendado=treino,
            tipo='confirmacao_presenca',
            lida=False
        ).update(lida=True)
        
        Frequencia.objects.update_or_create(
            usuario=usuario,
            data=timezone.now().date(),
            defaults={'status': 'PRESENTE'}
        )
        
        logger.info(f"Presença confirmada: {usuario.username} - Treino: {treino.tipo}")
        return confirmacao
    
    @staticmethod
    def verificar_treinos_hoje():
        """Verifica todos os treinos agendados para HOJE e envia notificações"""
        agora = timezone.now()
        dia_hoje = agora.strftime('%A').lower()
        
        dias_semana_map = {
            'sunday': 'domingo',
            'monday': 'segunda',
            'tuesday': 'terça', 
            'wednesday': 'quarta',
            'thursday': 'quinta',
            'friday': 'sexta',
            'saturday': 'sábado'
        }
        
        dia_hoje_ptbr = dias_semana_map.get(dia_hoje, '')
        
        usuarios_com_notificacoes = Perfil.objects.filter(notificacoes_ativadas=True)
        
        for perfil in usuarios_com_notificacoes:
            usuario = perfil.user
            
            treinos_hoje = Treino.objects.filter(
                usuario=usuario,
                dia_semana__iexact=dia_hoje_ptbr, 
                ativo=True
            )
            
            if treinos_hoje.exists():
                for treino in treinos_hoje:
                    GerenciadorNotificacoes.enviar_lembrete_treino(usuario, treino)
                    
                    notificacao_confirmacao_existente = Notificacao.objects.filter(
                        usuario=usuario,
                        treino_agendado=treino,
                        tipo='confirmacao_presenca',
                        data_criacao__date=agora.date()
                    ).exists()
                    
                    if not notificacao_confirmacao_existente:
                        GerenciadorNotificacoes.solicitar_confirmacao_presenca(usuario, treino)
            else:
                GerenciadorNotificacoes.enviar_notificacao_sem_treino(usuario)