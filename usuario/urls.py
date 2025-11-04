from django.urls import path
from . import views


urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path("login/", views.login_user, name="login"),
    path('menu/', views.menu_view, name='menu'),
    path('frequencia/', views.frequencia_view, name='frequencia'),
    path("menu/perfil/", views.perfil_usuario, name="perfil_usuario"),
    path('meusTreinos/', views.meus_treinos, name='meus_treinos'),
    path('meusTreinos/excluir/<int:id>/', views.excluir_treino, name='excluir_treino'),
    path('registrar-presenca/', views.registrar_presenca, name='registrar_presenca'),
    path("menu/criarAtleta/", views.criar_atleta, name="criar_atleta"),
    path("menu/excluirAtleta/", views.excluir_atleta, name="excluir_atleta"),
    path('api/get-frequencia/', views.get_frequencia_mes, name='get_frequencia_mes'),
    path("meusTreinos/editar/<int:id>/", views.editar_treino, name="editar_treino"),
    path('notificacoes/', views.listar_notificacoes, name='listar_notificacoes'),
    path('notificacoes/<int:notificacao_id>/ler/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('treino/<int:treino_id>/confirmar-presenca/', views.confirmar_presenca, name='confirmar_presenca'),
    path('configurar-notificacoes/', views.configurar_notificacoes, name='configurar_notificacoes'),
    path('notificacoes/<int:notificacao_id>/apagar/', views.apagar_notificacao, name='apagar_notificacao'),
]


