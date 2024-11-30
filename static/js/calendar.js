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
            $('#numero_guia').text(info.event.extendedProps.guia);

            const startDate = formatDate(info.event.start);
            const endDate = formatDate(info.event.end);

            $('#start_event_detail').text(startDate);
            $('#end_event_detail').text(endDate);
            $('#CalenderModalEdit').modal('show');

            $('#confirmEventBtn').off().click(function () {
                confirmEvent(info.event.id);
            });

            $('#deleteEventBtn').off().click(function () {
                deleteEvent(info.event.id);
            });
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
                var newEvent = {
                    id: response.id,
                    title: response.title,
                    start: response.start,
                    end: response.end,
                    backgroundColor: response.backgroundColor,
                    borderColor: response.borderColor,
                    extendedProps: {
                        paciente: response.paciente,
                        terapeuta: response.terapeuta,
                        guia: response.guia,
                        descricao: response.descricao
                    }
                };
                calendar.addEvent(newEvent);

                // Adicionar o evento à tabela dinamicamente
                addEventToTable(newEvent);

                $('#CalenderModalNew').modal('hide');
                $('#newEventForm')[0].reset();
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
});

