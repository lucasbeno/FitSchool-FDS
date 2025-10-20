// === LOGIN / DASHBOARD ===
function login() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
    closeAllModals();
}

// === MODAIS ===
function showRegister() {
    document.getElementById('registerModal').style.display = 'flex';
}

function showAddWorkoutModal() {
    const modal = document.getElementById('addWorkoutModal');
    if (modal) modal.style.display = 'flex';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// Fechar modal clicando fora
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

// === PERFIL DO USUÁRIO ===
document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.querySelector(".btn-action.edit");
    const profileForm = document.querySelector(".profile-details form");

    if (editBtn && profileForm) {
        editBtn.addEventListener("click", function (e) {
            e.preventDefault();
            profileForm.classList.add("editing");
        });
    }

    const cancelBtn = document.querySelector(".cancel-edit");
    if (cancelBtn && profileForm) {
        cancelBtn.addEventListener("click", function () {
            profileForm.classList.remove("editing");
        });
    }
});

// === CALENDÁRIO (simulação) ===
document.querySelectorAll('.calendar-day').forEach(day => {
    day.addEventListener('click', function () {
        if (this.classList.contains('present')) {
            this.classList.remove('present');
            this.classList.add('absent');
            this.querySelector('.day-status').textContent = 'Ausente';
        } else if (this.classList.contains('absent')) {
            this.classList.remove('absent');
            this.classList.add('present');
            this.querySelector('.day-status').textContent = 'Presente';
        }
    });
});

// === FORMULÁRIO DE TREINO (envio real) ===
document.addEventListener("DOMContentLoaded", function () {
    const workoutForm = document.querySelector("#addWorkoutModal form");
    if (workoutForm) {
        workoutForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(workoutForm);
            const response = await fetch("", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                closeModal("addWorkoutModal");
                location.reload(); // Recarrega pra mostrar o novo treino
            } else {
                alert("Erro ao salvar treino!");
            }
        });
    }
});

// === ADICIONAR NOVO EXERCÍCIO ===
document.addEventListener('DOMContentLoaded', function () {
    const addExerciseBtn = document.getElementById('add-exercise-btn');

    if (addExerciseBtn) {
        addExerciseBtn.addEventListener('click', function () {
            const container = document.getElementById('exercise-container');
            if (!container) return;

            const newForm = container.children[0].cloneNode(true);
            newForm.querySelectorAll('input').forEach(input => input.value = '');
            container.appendChild(newForm);
        });
    }
});

  document.querySelectorAll('.btn-icon-edit').forEach(button => {
  button.addEventListener('click', function () {
    const card = this.closest('.workout-card');
    const treinoId = card.dataset.treinoId; // ✅ ID direto do HTML

    // --- Dados básicos do treino ---
    const nome = card.querySelector('.workout-title').innerText;
    const tipo = card.querySelector('.workout-type').innerText;
    const dia = card.querySelector('.workout-detail:nth-child(1) span:last-child').innerText;
    const duracao = card.querySelector('.workout-detail:nth-child(2) span:last-child').innerText.replace(' min', '');
    const observacoes = card.querySelector('.workout-detail:nth-child(3) span:last-child').innerText;

    // --- Preenche os campos do modal ---
    document.getElementById('edit_nome').value = nome;
    document.getElementById('edit_tipo').value = tipo;
    document.getElementById('edit_dia_semana').value = dia;
    document.getElementById('edit_duracao').value = duracao;
    document.getElementById('edit_observacoes').value = observacoes === "—" ? "" : observacoes;

    // --- Define a action correta do formulário ---
    const form = document.getElementById('editWorkoutForm');
    form.action = `/user/menu/meusTreinos/editar/${treinoId}/`;

    // --- Atualiza lista de exercícios ---
    const container = document.getElementById('edit-exercise-container');
    container.innerHTML = ''; // limpa antes

    // ⚙️ Verifica se existem exercícios na estrutura
    const exerciciosContainer = card.querySelector('.workout-exercises ul');
    if (exerciciosContainer) {
      const exercicios = exerciciosContainer.querySelectorAll('li');
      exercicios.forEach((li, index) => {
        const texto = li.textContent.trim();
        if (texto.startsWith('Nenhum')) return;

        const [nome, resto] = texto.split(' — ');
        const [series, repeticoes] = resto ? resto.split('x') : ["", ""];

        container.innerHTML += `
          <div class="exercise-form">
            <div class="form-row">
              <div class="form-group">
                <label>Nome do Exercício</label>
                <input type="text" name="form-${index}-nome" value="${nome.trim()}">
              </div>
              <div class="form-group">
                <label>Séries</label>
                <input type="number" name="form-${index}-series" value="${series.trim()}">
              </div>
              <div class="form-group">
                <label>Repetições</label>
                <input type="number" name="form-${index}-repeticoes" value="${repeticoes.trim()}">
              </div>
            </div>
          </div>
        `;
      });
    } else {
      console.log("⚠️ Nenhum exercício encontrado para este treino.");
    }

    // --- Exibe o modal ---
    document.getElementById('editWorkoutModal').style.display = 'block';
  });
});

// --- Fechar modal ---
function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}
