from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    idade = models.PositiveIntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    meta = models.TextField(blank=True, null=True)
    
    # Novos campos para notificações
    notificacoes_ativadas = models.BooleanField(default=True)
    lembrete_minutos_antes = models.IntegerField(default=15, help_text="Minutos antes do treino para enviar lembrete")
    ultimo_lembrete_enviado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Frequencia(models.Model):
    STATUS_CHOICES = [
        ('PRESENTE', 'Presente'),
        ('AUSENTE', 'Ausente'),
        ('FOLGA', 'Folga'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('usuario', 'data')

    def __str__(self):
        return f"{self.usuario.username} - {self.data} - {self.status}"

class Atleta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="atleta")
    nome = models.CharField(max_length=150)
    apelido = models.CharField(max_length=50, blank=True)
    idade = models.PositiveIntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    objetivo = models.TextField(blank=True)

    @property
    def imc(self):
        if self.altura and self.peso and self.altura > 0:
            return float(self.peso) / (float(self.altura) ** 2)
        return None

    def __str__(self):
        return self.nome
    
class Treino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treinos')
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    dia_semana = models.CharField(max_length=20)
    duracao = models.PositiveIntegerField()
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Novos campos para agendamento de treinos
    data_hora = models.DateTimeField(null=True, blank=True, help_text="Data e hora específica do treino")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    
    @property
    def esta_agendado_hoje(self):
        """Verifica se o treino está agendado para hoje"""
        if self.data_hora:
            return self.data_hora.date() == timezone.now().date()
        return False
    
class Exercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    nome = models.CharField(max_length=100)
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.PositiveIntegerField(default=12)
    carga = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
         return f"{self.nome} ({self.series}x{self.repeticoes})"

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('lembrete_treino', 'Lembrete de Treino'),
        ('confirmacao_presenca', 'Confirmação de Presença'),
        ('sem_treino', 'Sem Treino Agendado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_envio = models.DateTimeField(null=True, blank=True)
    treino_agendado = models.ForeignKey(Treino, on_delete=models.SET_NULL, null=True, blank=True, related_name='notificacoes')
    
    class Meta:
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"

class ConfirmacaoPresenca(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmacoes')
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='confirmacoes')
    confirmado = models.BooleanField(default=False)
    data_confirmacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'treino']
    
    def __str__(self):
        status = "Confirmado" if self.confirmado else "Pendente"
        return f"{self.usuario.username} - {self.treino.nome} - {status}"