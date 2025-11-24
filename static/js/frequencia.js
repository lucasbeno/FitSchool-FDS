// frequencia.js (Versão Corrigida com as URLs corretas)

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. SELEÇÃO DOS ELEMENTOS DO DOM ---
    const modal = document.getElementById('presence-modal');
    const openModalBtn = document.getElementById('register-presence-btn');
    const closeModalBtn = document.querySelector('.close-button');
    const presenceForm = document.getElementById('presence-form');
    const dateInput = document.getElementById('date-input');
    const calendarGrid = document.getElementById('calendar-grid');
    const calendarTitle = document.getElementById('calendar-title');
    const prevMonthBtn = document.getElementById('prev-month-btn');
    const nextMonthBtn = document.getElementById('next-month-btn');

    let currentYear;
    let currentMonth;

    // --- 2. LÓGICA DA JANELA MODAL ---
    
    const openModal = () => {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
        modal.style.display = 'flex';
    };

    const closeModal = () => {
        modal.style.display = 'none';
    };

    openModalBtn.addEventListener('click', openModal);
    closeModalBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            closeModal();
        }
    });

    // --- 3. LÓGICA DE GERAÇÃO E NAVEGAÇÃO DO CALENDÁRIO ---

    const applyAttendanceData = (attendanceData) => {
        for (const dateStr in attendanceData) {
            const dayCell = document.querySelector(`.calendar-day[data-date="${dateStr}"]`);
            const status = attendanceData[dateStr];
            if (dayCell && status) {
                dayCell.classList.remove('presente', 'ausente', 'folga');
                dayCell.classList.add(status.toLowerCase());
                let statusSpan = dayCell.querySelector('.day-status');
                if (!statusSpan) {
                    statusSpan = document.createElement('div');
                    statusSpan.className = 'day-status';
                    dayCell.appendChild(statusSpan);
                }
                statusSpan.textContent = status;
            }
        }
    };

    const loadAttendanceData = (year, month) => {
        // CORREÇÃO 1: Adicionado o prefixo '/user/menu/' à URL da API
        fetch(`/user/menu/api/get-frequencia/?year=${year}&month=${month + 1}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                applyAttendanceData(data);
            })
            .catch(error => console.error('Erro ao carregar dados de frequência:', error));
    };

    const generateCalendar = (year, month) => {
        const monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
        calendarTitle.textContent = `${monthNames[month]} de ${year}`;
        const weekdayHeaders = calendarGrid.querySelectorAll('.calendar-weekday');
        calendarGrid.innerHTML = '';
        weekdayHeaders.forEach(header => calendarGrid.appendChild(header));
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        for (let i = 0; i < firstDayOfMonth; i++) {
            calendarGrid.appendChild(document.createElement('div'));
        }
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'calendar-day';
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dayCell.dataset.date = dateStr;
            dayCell.innerHTML = `<div class="day-number">${day}</div>`;
            calendarGrid.appendChild(dayCell);
        }
        loadAttendanceData(year, month);
    };

    nextMonthBtn.addEventListener('click', () => {
        currentMonth++;
        if (currentMonth > 11) { currentMonth = 0; currentYear++; }
        generateCalendar(currentYear, currentMonth);
    });

    prevMonthBtn.addEventListener('click', () => {
        currentMonth--;
        if (currentMonth < 0) { currentMonth = 11; currentYear--; }
        generateCalendar(currentYear, currentMonth);
    });
    
    // --- 4. SUBMISSÃO DO FORMULÁRIO (FETCH API) ---
    
    presenceForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const selectedDate = dateInput.value;
        const selectedStatus = document.querySelector('input[name="status"]:checked').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // CORREÇÃO 2: Adicionado o prefixo '/user/menu/' também aqui
        fetch('/user/menu/registrar-presenca/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
            body: JSON.stringify({ date: selectedDate, status: selectedStatus })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                closeModal();
                applyAttendanceData({ [selectedDate]: selectedStatus });
                document.getElementById('dias-presentes').textContent = data.updated_stats.dias_presentes;
                document.getElementById('dias-ausentes').textContent = data.updated_stats.dias_ausentes;
                document.getElementById('taxa-frequencia').textContent = `${data.updated_stats.taxa_frequencia}%`;
            } else {
                alert('Ocorreu um erro: ' + data.message);
            }
        })
        .catch(error => console.error('Erro na requisição:', error));
    });

  
    const today = new Date();
    currentYear = today.getFullYear();
    currentMonth = today.getMonth();
    generateCalendar(currentYear, currentMonth);
});

