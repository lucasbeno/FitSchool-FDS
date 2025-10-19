from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime
import json

from .forms import RegistroForm, AtletaForm, TreinoForm, ExercicioFormSet
from .models import Frequencia, Atleta, Treino, Exercicio

from .models import Treino, Exercicio
from .forms import TreinoForm, ExercicioFormSet



@login_required
def frequencia_view(request):
    # Esta parte calcula as estatísticas para os cards na primeira vez que a página carrega.
    frequencias = Frequencia.objects.filter(usuario=request.user)
    
    dias_presentes = frequencias.filter(status='PRESENTE').count()
    dias_ausentes = frequencias.filter(status='AUSENTE').count()
    total_dias = dias_presentes + dias_ausentes
    taxa_frequencia = (dias_presentes / total_dias * 100) if total_dias > 0 else 0

    context = {
        'dias_presentes': dias_presentes,
        'dias_ausentes': dias_ausentes,
        'taxa_frequencia': round(taxa_frequencia),
    }
    # Certifique-se que o nome do template aqui está correto
    return render(request, 'fitschool/pages/frequencia.html', context)


@login_required
def get_frequencia_mes(request):
    """
    Esta view responde às requisições do JavaScript para fornecer os dados de 
    frequência de um mês/ano específico.
    """
    if request.method == 'GET':
        try:
            year = int(request.GET.get('year'))
            month = int(request.GET.get('month'))

            # Filtra as frequências para o usuário logado, no ano e mês especificados
            frequencias = Frequencia.objects.filter(
                usuario=request.user, # Ajustado para o seu modelo
                data__year=year,
                data__month=month
            )

            # Formata os dados para o JavaScript no formato {"AAAA-MM-DD": "STATUS"}
            dados_frequencia = {
                f.data.strftime('%Y-%m-%d'): f.status
                for f in frequencias
            }

            return JsonResponse(dados_frequencia)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Ano e mês inválidos.'}, status=400)
    
    return JsonResponse({'error': 'Método inválido.'}, status=405)

@login_required
@require_POST # Garante que esta view só aceite requisições POST
def registrar_presenca(request):
    try:
        # Pega os dados enviados pelo JavaScript
        data = json.loads(request.body)
        data_selecionada = data.get('date')
        status_selecionado = data.get('status')

        # Converte a data string para um objeto date
        data_obj = datetime.strptime(data_selecionada, '%Y-%m-%d').date()

        frequencia, created = Frequencia.objects.update_or_create(
            usuario=request.user,
            data=data_obj,
            defaults={'status': status_selecionado}
        )
        
        frequencias = Frequencia.objects.filter(usuario=request.user)
        dias_presentes = frequencias.filter(status='PRESENTE').count()
        dias_ausentes = frequencias.filter(status='AUSENTE').count()
        total_dias = dias_presentes + dias_ausentes
        taxa_frequencia = (dias_presentes / total_dias * 100) if total_dias > 0 else 0

        return JsonResponse({
            'status': 'success',
            'message': 'Frequência registrada com sucesso!',
            'updated_stats': {
                'dias_presentes': dias_presentes,
                'dias_ausentes': dias_ausentes,
                'taxa_frequencia': round(taxa_frequencia)
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("menu")  
        else:
            messages.error(request, "Usuário ou senha inválidos")
            return redirect("home")  

    return redirect("home")

def registrar(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menu")
    else:
        form = RegistroForm()
    return render(request, "fitschool/pages/registro.html", {"form": form})

def menu_view(request):
    return render(request, "fitschool/pages/menu.html")



def meus_treinos(request):
    return render(request, "fitschool/pages/treino.html")

def criar_Atleta(request):
    return render(request, "fitschool/pages/criarAtleta.html")

@login_required
def criar_atleta(request):
    if hasattr(request.user, "atleta"):
        # Já existe atleta → não deixa recriar
        return redirect("perfil_usuario")

    if request.method == "POST":
        form = AtletaForm(request.POST)
        if form.is_valid():
            atleta = form.save(commit=False)
            atleta.user = request.user
            atleta.save()
            return redirect("perfil_usuario")
    else:
        form = AtletaForm()

    return render(request, "fitschool/pages/criarAtleta.html", {"form": form})

@login_required
def perfil_usuario(request):
    atleta = getattr(request.user, "atleta", None)
    if not atleta:
        return redirect("criar_atleta")

    if request.method == "POST":
        form = AtletaForm(request.POST, instance=atleta)
        if form.is_valid():
            form.save()
            return redirect("perfil_usuario")
    else:
        form = AtletaForm(instance=atleta)

    return render(request, "fitschool/pages/perfilUsuario.html", {
        "atleta": atleta,
        "form": form
    })

@login_required
def editar_atleta(request):
    atleta = getattr(request.user, "atleta", None)
    if not atleta:
        return redirect("criar_atleta")

    if request.method == "POST":
        form = AtletaForm(request.POST, instance=atleta)
        if form.is_valid():
            form.save()
            return redirect("perfil_usuario")
    else:
        form = AtletaForm(instance=atleta)

    return render(request, "fitschool/pages/editarAtleta.html", {"form": form})

@login_required
def excluir_atleta(request):
    atleta = getattr(request.user, "atleta", None)
    if request.method == "POST" and atleta:
        atleta.delete()
        return redirect("menu")  # manda pro dashboard
    return render(request, "fitschool/pages/confirmar_delete.html", {"atleta": atleta})

@login_required
def meus_treinos(request):
    treinos = Treino.objects.filter(usuario=request.user)
    form = TreinoForm()
    exercicio_formset = ExercicioFormSet(queryset=Exercicio.objects.none())

    if request.method == 'POST':
        form = TreinoForm(request.POST)
        exercicio_formset = ExercicioFormSet(request.POST)

        if form.is_valid() and exercicio_formset.is_valid():
            treino = form.save(commit=False)
            treino.usuario = request.user
            treino.save()

            # Salva todos os exercícios vinculados ao treino
            for exercicio_form in exercicio_formset:
                if exercicio_form.cleaned_data:
                    exercicio = exercicio_form.save(commit=False)
                    exercicio.treino = treino
                    exercicio.save()

            return redirect('meus_treinos')

    return render(request, 'fitschool/pages/treino.html', {
        'treinos': treinos,
        'form': form,
        'exercicio_formset': exercicio_formset
    })

@login_required
def excluir_treino(request, id):
    treino = get_object_or_404(Treino, id=id, usuario=request.user)
    treino.delete()
    return redirect('meus_treinos')

@login_required
def editar_treino(request, id):
    treino = get_object_or_404(Treino, id=id, usuario=request.user)

    if request.method == "POST":
        # Atualiza informações básicas do treino
        treino.nome = request.POST.get("nome", treino.nome)
        treino.tipo = request.POST.get("tipo", treino.tipo)
        treino.dia_semana = request.POST.get("dia_semana", treino.dia_semana)
        treino.duracao = request.POST.get("duracao", treino.duracao)
        treino.observacoes = request.POST.get("observacoes", treino.observacoes)
        treino.save()

        # 🟢 Apaga os exercícios antigos
        treino.exercicios.all().delete()

        # 🟢 Recria com base nos dados vindos do formulário
        total = int(request.POST.get("form-TOTAL_FORMS", 0))
        for i in range(total):
            nome = request.POST.get(f"form-{i}-nome")
            series = request.POST.get(f"form-{i}-series")
            repeticoes = request.POST.get(f"form-{i}-repeticoes")
            carga = request.POST.get(f"form-{i}-carga")  # caso você adicione esse campo depois

            if nome and series and repeticoes:
                Exercicio.objects.create(
                    treino=treino,
                    nome=nome.strip(),
                    series=int(series),
                    repeticoes=int(repeticoes),
                    carga=carga or None,
                )

        return redirect("meus_treinos")

    return redirect("meus_treinos")
