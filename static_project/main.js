$(document).ready(function () {
    $('#modal-btn').click(function () {
        $('#modal1')
            .modal('show')
        ;
    })
    $('#modal-btn2').click(function () {
        $('#modal2')
            .modal('show')
        ;
    })
    $('#modal-btn3').click(function () {
        $('#modal3')
            .modal('show')
        ;
    })
    $('.ui.dropdown').dropdown()
    $('.special.cards .image').dimmer({
      on: 'hover'
    });
})