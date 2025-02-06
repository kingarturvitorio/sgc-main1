FullCalendar.globalLocales.push(function () {
    'use strict';

    var ptBr = {
        code: 'pt-br',
        week: {
            dow: 1, // Monday is the first day of the week.
            doy: 4 // The week that contains Jan 4th is the first week of the year.
        },
        buttonText: {
            prev: 'Anterior',
            next: 'Próximo',
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia',
            list: 'Agenda'
        },
        weekText: 'Sm',
        allDayText: 'Dia inteiro',
        moreLinkText: function (n) {
            return 'mais +' + n;
        },
        noEventsText: 'Não há eventos para mostrar'
    };

    return ptBr;

}());


function formatDate(date) {
    if (!(date instanceof Date)) {
        return 'Data inválida';  // Mensagem de erro caso a data não seja um objeto válido
    }
    return date.toLocaleString('pt-BR', {
        weekday: 'long',  // Dia da semana
        year: 'numeric',   // Ano
        month: 'long',     // Mês
        day: 'numeric',    // Dia
        hour: '2-digit',   // Hora
        minute: '2-digit', // Minutos
        hour12: false      // Formato de 24 horas
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
<<<<<<< HEAD
    
=======
>>>>>>> 8051eacca80926afeee9b02002f8811a1de471c7
    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,list'
        },
        events: fetchEvents,
        selectable: true,
        select: () => $('#CalenderModalNew').modal('show'),
        eventClick: handleEventClick,
        eventDidMount: customizeEventAppearance
    });

    calendar.render();
<<<<<<< HEAD
        // Buscar terapeutas ao carregar a página
    console.log("Iniciando requisição para obter terapeutas...");
    $.ajax({
        type: 'GET',
        url: '/get_terapeutas/',  // Certifique-se de que essa URL está correta
        success: function(data) {
            console.log("Terapeutas recebidos:", data);  // Depuração

            let select = document.getElementById('terapeutaFilter');
            if (!select) {
                console.error("Elemento #terapeutaFilter não encontrado!");
                return;
            }

            select.innerHTML = '<option value="">Selecione um Terapeuta</option>'; // Resetando opções

            data.forEach(terapeuta => {
                let option = document.createElement('option');
                option.value = terapeuta.nome_terapeuta;
                option.textContent = terapeuta.nome_terapeuta;
                select.appendChild(option);
            });
        },
        error: function(xhr, status, error) {
            console.error('Erro ao buscar terapeutas:', error);
        }
    });    
    
    // Event form submission
    $('#newEventForm').on('submit', handleNewEventSubmission);
    
=======

    // Event form submission
    $('#newEventForm').on('submit', handleNewEventSubmission);
>>>>>>> 8051eacca80926afeee9b02002f8811a1de471c7

        // Show All Events Button
    document.getElementById('showAllEventsButton').addEventListener('click', function() {
        calendar.removeAllEvents();  // Clear existing events
        calendar.refetchEvents(); // This will fetch all events again
    });

    async function fetchEvents(fetchInfo, successCallback, failureCallback) {
        try {
            const response = await $.ajax({
                url: '/get/event/',
<<<<<<< HEAD
                method: 'GET',
                data: {
                    start_date: fetchInfo.startStr, // Passando o intervalo de datas
                    end_date: fetchInfo.endStr
                }
=======
                method: 'GET'
>>>>>>> 8051eacca80926afeee9b02002f8811a1de471c7
            });
            successCallback(response);
        } catch (error) {
            console.error('Erro ao carregar eventos: ', error);
            failureCallback(error);
        }
    }

    function handleEventClick(info) {
        const { extendedProps } = info.event;
        $('#nome_paciente').text(extendedProps.paciente);
        $('#nome_terapeuta').text(extendedProps.terapeuta);
        $('#nome_convenio').text(extendedProps.convenio);
        $('#numero_guia').text(extendedProps.guia);
        $('#start_event_detail').text(formatDate(info.event.start));
        $('#end_event_detail').text(formatDate(info.event.end));
        $('#CalenderModalEdit').modal('show');

        const pacienteId = extendedProps.paciente_id;
        $('#deleteAllEventsBtn').data('paciente-id', pacienteId);

        $('#confirmEventBtn').off().click(() => confirmEvent(info.event.id));
        $('#deleteEventBtn').off().click(() => deleteEvent(info.event.id));
        $('#deleteAllEventsBtn').off().click(() => deleteAllEvents(pacienteId));
    }

    function customizeEventAppearance(info) {
        if (info.event.extendedProps.terapeuta) {
            info.el.style.backgroundColor = info.event.backgroundColor;
            info.el.style.color = 'white';
        }
    }

    async function handleNewEventSubmission(e) {
        e.preventDefault();
        const formData = $(this).serialize();

        try {
            const response = await $.ajax({
                type: 'POST',
                url: `/event/new/`,
                data: formData
            });
        // Refetch events to get the latest data from the server
        calendar.refetchEvents();
        $('#CalenderModalNew').modal('hide');
        $('#newEventForm')[0].reset();
        } catch (error) {
        console.error('Erro ao criar evento: ', error);
        }
        }


    
    // Function to confirm event via AJAX
    function confirmEvent(eventId) {
        $.ajax({
            type: 'POST',
            url: `/confirm_event/${eventId}/`,
            data: { 'csrfmiddlewaretoken': csrfToken },
            success: function (response) {
                calendar.refetchEvents();
                $('#CalenderModalEdit').modal('hide');
                $('#newEventForm')[0].reset();
            },
            error: function (xhr, status, error) {
                console.error('Error confirming event: ', error);
            }
        });
    }

    // Função para deletar evento via AJAX e remover da tabela
    function deleteEvent(eventId) {
        $.ajax({
            type: 'POST',
            url: `/delete_event/${eventId}/`,
            data: { 'csrfmiddlewaretoken': csrfToken },
            success: function () {
                // Remove o evento do calendário
                var event = calendar.getEventById(eventId);
                event.remove();

                // Remove a linha correspondente na tabela
                $(`#eventRow-${eventId}`).remove();

                $('#CalenderModalEdit').modal('hide');
            },
            error: function (xhr, status, error) {
                console.error('Erro ao excluir o evento: ', error);
            }
        });
    }

        // Função para deletar todos os eventos de um paciente
    function deleteAllEvents(pacienteId) {
        $.ajax({
            type: 'POST',
            url: `/event/delete_all/${pacienteId}/`,  // A URL da sua view Django
            data: { 'csrfmiddlewaretoken': csrfToken },
            success: function(response) {
                if (response.success) {
                    // Remove todos os eventos do paciente do calendário
                    calendar.getEvents().forEach(function(event) {
                        if (event.extendedProps.paciente_id === pacienteId) {
                            event.remove(); // Remove o evento do calendário
                        }
                    });

                                    // Fecha o modal e reseta o formulário
                    $('#CalenderModalEdit').modal('hide');
                    // Exibir mensagem de sucesso
                } else {
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Erro ao deletar eventos:', error);
                alert('Ocorreu um erro ao tentar deletar os eventos.');
            }
        });
    }

     // Filter button functionality
     document.getElementById('filterButton').addEventListener('click', function() {
<<<<<<< HEAD
        const terapeutaNome = document.getElementById('terapeutaFilter').value; // Nome do terapeuta selecionado
    
        // Obtendo a visualização atual do calendário
        var currentView = calendar.view.type;
        var startDate = calendar.view.currentStart; // Data de início da visualização
        var endDate = calendar.view.currentEnd; // Data de fim da visualização
    
        console.log('Visualização Atual:', currentView);
        console.log('Intervalo:', startDate, 'até', endDate);
    
        $.ajax({
            type: 'GET',
            url: '/filter_events/', // URL no Django
            data: {
                'terapeuta_nome': terapeutaNome,
                'start_date': startDate.toISOString(),  // Converte para string ISO (YYYY-MM-DD)
                'end_date': endDate.toISOString(),
                'view_type': currentView // Passa o tipo de visualização
            },
            success: function(data) {
                console.log('Eventos Filtrados:', data);
                calendar.removeAllEvents();
                data.forEach(eventData => {
                    calendar.addEvent(eventData);
                });
            },
            error: function(xhr, status, error) {
                console.error('Erro ao buscar eventos:', error);
            }
        });
    });
    

    
=======
        const terapeutaNome = document.getElementById('terapeutaFilter').value;  // Get the selected therapist name
        console.log('Selected Therapist:', terapeutaNome);  // Debugging line
        
        $.ajax({
            type: 'GET',
            url: '/filter_events/',  // Ensure this matches your Django URL
            data: { 'terapeuta_nome': terapeutaNome },
            success: function(data) {
                console.log('Fetched Events:', data);  // Debugging line
                calendar.removeAllEvents();  // Clear existing events

                data.forEach(eventData => {
                    calendar.addEvent(eventData);  // Add the filtered events to the calendar
                });
            },
            error: function(xhr, status, error) {
                console.error('Error fetching filtered events: ', error);
            }
        });
    });

>>>>>>> 8051eacca80926afeee9b02002f8811a1de471c7
    //funções de busca de paciente e terapeuta
    $(document).ready(function () {
        $("#paciente").on("input", function () {
            var query = $(this).val();  // Obter o valor digitado no campo paciente
            if (query.length > 1) {  // Começar a busca após 3 caracteres digitados
                $.ajax({
                    url: `/buscar-pacientes/`,
                    data: {
                        'q': query,
                    },
                    success: function (data) {
                        var suggestionsList = $("#paciente-suggestions");
                        suggestionsList.empty(); // Limpa as sugestões anteriores
                        
                        if (data.length > 0) {
                            data.forEach(function (paciente) {
                                suggestionsList.append('<li class="list-group-item" data-id="' + paciente.id + '">' + paciente.nome + '</li>');
                            });
                            suggestionsList.show();  // Exibe as sugestões
                        } else {
                            suggestionsList.hide();  // Oculta se não houver resultados
                        }
                    },
                    error: function () {
                        alert("Erro ao buscar pacientes.");
                    }
                });
            } else {
                $("#paciente-suggestions").hide();  // Oculta se o campo estiver vazio
            }
        });

        // Quando o usuário clicar em uma sugestão, preencher o campo de paciente
        $("#paciente-suggestions").on("click", "li", function () {
            var pacienteNome = $(this).text();
            var pacienteId = $(this).data("id");
            $("#paciente").val(pacienteNome);  // Preenche o campo com o nome
            // Você pode salvar o pacienteId em um campo escondido ou usá-lo como preferir
            $("#paciente-suggestions").hide();  // Oculta a lista de sugestões
        });
    });

    $(document).ready(function () {
        $("#terapeuta").on("input", function () {
            var query = $(this).val();  // Obter o valor digitado no campo paciente
            if (query.length > 1) {  // Começar a busca após 3 caracteres digitados
                $.ajax({
                    url: `/buscar-terapeutas/`,
                    data: {
                        'q': query,
                    },
                    success: function (data) {
                        var suggestionsList = $("#terapeuta-suggestions");
                        suggestionsList.empty(); // Limpa as sugestões anteriores
                        
                        if (data.length > 0) {
                            data.forEach(function (terapeuta) {
                                suggestionsList.append('<li class="list-group-item" data-id="' + terapeuta.id + '">' + terapeuta.nome_terapeuta + '</li>');
                            });
                            suggestionsList.show();  // Exibe as sugestões
                        } else {
                            suggestionsList.hide();  // Oculta se não houver resultados
                        }
                    },
                    error: function () {
                        alert("Erro ao buscar terapeuta.");
                    }
                });
            } else {
                $("#terapeuta-suggestions").hide();  // Oculta se o campo estiver vazio
            }
        });

        // Quando o usuário clicar em uma sugestão, preencher o campo de paciente
        $("#terapeuta-suggestions").on("click", "li", function () {
            var terapeutaNome = $(this).text();
            var terapeutaId = $(this).data("id");
            $("#terapeuta").val(terapeutaNome);  // Preenche o campo com o nome
            // Você pode salvar o pacienteId em um campo escondido ou usá-lo como preferir
            $("#terapeuta-suggestions").hide();  // Oculta a lista de sugestões
        });
    });
});


