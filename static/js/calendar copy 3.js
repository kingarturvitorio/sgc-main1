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
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,list'
        },
        // Carregando eventos via AJAX
        events: function (fetchInfo, successCallback, failureCallback) {
            $.ajax({
                url: '/get/event/', // URL da view que retorna os eventos em JSON
                method: 'GET',
                success: function (data) {
                    successCallback(data); // Passa os eventos recebidos ao calendário
                },
                error: function (xhr, status, error) {
                    console.error('Erro ao carregar eventos: ', error);
                    failureCallback(error);
                }
            });
        },
        selectable: true,
        select: function (info) {
            $('#CalenderModalNew').modal('show');
        },
        eventClick: function (info) {
            $('#nome_paciente').text(info.event.extendedProps.paciente);
            $('#nome_terapeuta').text(info.event.extendedProps.terapeuta);
            $('#nome_convenio').text(info.event.extendedProps.convenio);
            $('#numero_guia').text(info.event.extendedProps.guia);

            const startDate = formatDate(info.event.start);
            const endDate = formatDate(info.event.end);

            $('#start_event_detail').text(startDate);
            $('#end_event_detail').text(endDate);
            $('#CalenderModalEdit').modal('show');

            // Atualiza o paciente ID no botão de deletar todos os eventos
            var pacienteId = info.event.extendedProps.paciente_id;  // Pega o paciente ID do evento
            console.log("Paciente ID: ", pacienteId);  // Verifica o valor do ID no console
            
            $('#deleteAllEventsBtn').data('paciente-id', pacienteId);  // Atualiza o paciente_id

            $('#confirmEventBtn').off().click(function () {
                confirmEvent(info.event.id);
            });

            $('#deleteEventBtn').off().click(function () {
                deleteEvent(info.event.id);
            });

            $('#deleteAllEventsBtn').off().click(function () {
                var pacienteId = $(this).data('paciente-id');  // Pega o pacienteId atualizado
                console.log("ID do Paciente no clique: ", pacienteId);  // Verifica o valor do ID no clique
                deleteAllEvents(pacienteId);
            });
        },

        eventDidMount: function(info) {
            // Adiciona uma lógica extra para personalizar as cores, se necessário
            if (info.event.extendedProps.terapeuta) {
                info.el.style.backgroundColor = info.event.backgroundColor; // Aplica a cor dinâmica
                info.el.style.color = 'white'; // Ajusta o texto para ficar legível
            }
        }
    });
    calendar.render();

        // Função para adicionar novo evento via AJAX
        $('#newEventForm').on('submit', function (e) {
            e.preventDefault();
            var formData = $(this).serialize();
    
            $.ajax({
                type: 'POST',
                url: `/event/new/`,
                data: formData,
                success: function (response) {
                    // Adiciona o evento original ao calendário
                    var originalEvent = {
                        id: response.id,  // Ajuste conforme a estrutura da resposta
                        title: response.title,
                        start: response.start,
                        end: response.end,
                        backgroundColor: response.backgroundColor,
                        borderColor: response.borderColor,
                        extendedProps: {
                            paciente: response.paciente,
                            terapeuta: response.terapeuta,
                            convenio: response.convenio,
                            guia: response.guia,
                            descricao: response.descricao
                        }
                    };
                    calendar.addEvent(originalEvent);
    
                    // Adiciona os eventos replicados ao calendário (verifica se existe o campo replicated_events)
                    if (Array.isArray(response.replicated_events)) {
                        response.replicated_events.forEach(function (replicatedEvent) {
                            var newReplicatedEvent = {
                                id: replicatedEvent.id,
                                title: replicatedEvent.title,
                                start: replicatedEvent.start,
                                end: replicatedEvent.end,
                                backgroundColor: replicatedEvent.backgroundColor,
                                borderColor: replicatedEvent.borderColor
                            };
                            calendar.addEvent(newReplicatedEvent);
                        });
                    }
                    
                    // Força o calendário a renderizar novamente
                    // Após adicionar os eventos replicados
                    calendar.refetchEvents();  // Refetch eventos do backend ou renderiza todos os eventos adicionados
    
                    // Adicionar o evento original à tabela dinamicamente
                    addEventToTable(originalEvent);
    
                    // Fecha o modal e reseta o formulário
                    $('#CalenderModalNew').modal('hide'); // Certifique-se que o ID está correto
                    $('#newEventForm')[0].reset(); // Reseta o formulário
                },
                error: function (xhr, status, error) {
                    console.error('Erro ao criar evento: ', error);
                }
            });
        });

    
    // Função para adicionar uma linha na tabela
    function addEventToTable(event) {
        var startDate = new Date(event.start);
        var formattedDate = startDate.toLocaleString('pt-BR', { dateStyle: 'full', timeStyle: 'short' });

        // Criando nova linha e atribuindo o id da linha correspondente ao evento
        var newRow = `<tr id="eventRow-${event.id}">
                            <td>${event.extendedProps.paciente}</td>
                            <td>${event.extendedProps.terapeuta}</td>
                            <td>${event.extendedProps.guia}</td>
                            <td>${formattedDate}</td>
                        </tr>`;

        // Adicionando a nova linha na tabela
        $('#eventTableBody').append(newRow);
    }

    // Função para confirmar evento via AJAX
    function confirmEvent(eventId) {
        $.ajax({
            type: 'POST',
            url: `/confirm_event/${eventId}/`,
            data: { 'csrfmiddlewaretoken': csrfToken },
            success: function () {
                var event = calendar.getEventById(eventId);
                event.setProp('backgroundColor', 'green');
                event.setProp('borderColor', 'green');
                $('#CalenderModalEdit').modal('hide');
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

