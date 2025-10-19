from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    idade = models.PositiveIntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    meta = models.TextField(blank=True, null=True)  

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

    def __str__(self):
        return self.nome
    
class Exercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    nome = models.CharField(max_length=100)
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.PositiveIntegerField(default=12)
    carga = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
         return f"{self.nome} ({self.series}x{self.repeticoes})"
    