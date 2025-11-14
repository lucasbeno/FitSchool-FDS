document.addEventListener("DOMContentLoaded", function () {
    window.showAddWorkoutModal = function() {
        const modal = document.getElementById('addWorkoutModal');
        if (modal) modal.style.display = 'flex';
    }

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'none';
    }

    window.addEventListener('click', function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });

    const addExerciseBtn = document.getElementById('add-exercise-btn');
    if (addExerciseBtn) {
        addExerciseBtn.addEventListener('click', function () {
            const container = document.getElementById('exercise-container');
            const managementForm = document.querySelector('#addWorkoutModal input[name="form-TOTAL_FORMS"]');
            if (!container || !managementForm) {
                console.error("Não foi possível encontrar o container de exercícios ou o management form.");
                return;
            }

            const totalForms = parseInt(managementForm.value);
            const formTemplate = container.querySelector('.exercise-form').innerHTML;
            const newFormHtml = formTemplate.replace(/form-0/g, `form-${totalForms}`);
            
            const newDiv = document.createElement('div');
            newDiv.className = 'exercise-form';
            newDiv.innerHTML = newFormHtml;
            newDiv.querySelectorAll('input').forEach(input => input.value = '');
            
            container.appendChild(newDiv);
            managementForm.value = totalForms + 1; 
        });
    }

    const workoutForm = document.querySelector("#addWorkoutModal form");
    if (workoutForm) {
        workoutForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(workoutForm);

            const response = await fetch(workoutForm.action, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                closeModal("addWorkoutModal");
                location.reload(); 
            } else {
                alert("Erro ao salvar treino!");
            }
        });
    }

    document.querySelectorAll('.btn-icon-edit').forEach(button => {
        button.addEventListener('click', function () {
            const card = this.closest('.workout-card');
            const treinoId = card.dataset.treinoId;

            document.getElementById('edit_nome').value = card.querySelector('.workout-title').innerText;
            document.getElementById('edit_tipo').value = card.querySelector('.workout-type').innerText;
            document.getElementById('edit_dia_semana').value = card.querySelector('.workout-detail:nth-child(1) span:last-child').innerText;
            document.getElementById('edit_duracao').value = card.querySelector('.workout-detail:nth-child(2) span:last-child').innerText.replace(' min', '');
            const obsText = card.querySelector('.workout-detail:nth-child(3) span:last-child').innerText;
            document.getElementById('edit_observacoes').value = (obsText === "—") ? "" : obsText;

            const form = document.getElementById('editWorkoutForm');
            form.action = this.dataset.actionUrl; 

            const container = document.getElementById('edit-exercise-container');
            container.innerHTML = '';
            const exercicios = card.querySelectorAll('.workout-exercises ul li');
            let exercisesHtml = '';
            let validExercisesCount = 0;

            exercicios.forEach((li, index) => {
                const texto = li.textContent.trim();
                if (texto.startsWith('Nenhum')) return;

                const exercicioId = li.dataset.exercicioId;
                const [nome, resto] = texto.split(' — ');
                const [series, repeticoesComCarga] = resto.split('x');
                const repeticoes = repeticoesComCarga.split('(')[0].trim();
                const cargaMatch = repeticoesComCarga.match(/\(([^)]+)\)/);
                const carga = cargaMatch ? cargaMatch[1] : '';

                exercisesHtml += `
                    <div class="exercise-form">
                        <input type="hidden" name="form-${index}-id" value="${exercicioId}">
                        <input type="hidden" name="form-${index}-treino" value="${treinoId}">
                        <div class="form-row">
                            <div class="form-group"><label>Nome</label><input type="text" name="form-${index}-nome" value="${nome.trim()}"></div>
                            <div class="form-group"><label>Séries</label><input type="number" name="form-${index}-series" value="${series.trim()}"></div>
                            <div class="form-group"><label>Repetições</label><input type="number" name="form-${index}-repeticoes" value="${repeticoes.trim()}"></div>
                            <div class="form-group"><label>Carga</label><input type="text" name="form-${index}-carga" value="${carga.trim()}"></div>
                        </div>
                    </div>`;
                validExercisesCount++;
            });
            container.innerHTML = exercisesHtml;

            const totalFormsInput = document.querySelector('#editWorkoutModal input[name="form-TOTAL_FORMS"]');
            const initialFormsInput = document.querySelector('#editWorkoutModal input[name="form-INITIAL_FORMS"]');
            if (totalFormsInput && initialFormsInput) {
                totalFormsInput.value = validExercisesCount;
                initialFormsInput.value = validExercisesCount;
            }

            document.getElementById('editWorkoutModal').style.display = 'block';
        });
    });

    const favoriteButtons = document.querySelectorAll('.btn-icon-favorite');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const button = this;
            const treinoId = button.dataset.treinoId;
            
            const csrfToken = document.querySelector('#addWorkoutModal form [name=csrfmiddlewaretoken]').value;
            
            fetch(`/user/menu/treino/favoritar/${treinoId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na rede ou no servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const icon = button.querySelector('i');
                    if (data.favorito) {
                        button.classList.add('is-favorito');
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                    } else {
                        button.classList.remove('is-favorito');
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao favoritar:', error);
                alert('Ocorreu um erro ao favoritar. Verifique o console.');
            });
        });
    });

});