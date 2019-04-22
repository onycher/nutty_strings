var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function() {
    socket.emit('request-test-suites', {});
    socket.emit('request-strings', {});
});

socket.on('test-suites', function(json) {
    console.log(json);
    $('#test-suites').html(json.data);
});

socket.on('tests', function(json) {
    $('#test-cases').html(json.data);
});

socket.on('strings', function(json) {
    console.log(json);
    $('#string-table').html(json.data);

    $('tr').each(function() {
        $(this).click(function() {
            socket.emit('run', {id: $(this).attr('value'),
                test: $('#test-cases').val(),
                suite: $('#test-suites').val()});
            console.log($(this).attr('value'));
        });
    });
});


$('#test-suites').change(function() {
    var val = $('#test-suites').val();
    if (val == 'Plugin') {
        $('#toggle-test-suite').addClass('disabled');
        $('#test-cases-row').hide();
        $('#strings-row').hide();
    }
    else {
        $('#toggle-test-suite').removeClass('disabled');
        socket.emit('request-tests', {data: val})
        $('#test-cases-row').show();
        $('#strings-row').show();
    }
    console.log($('#test-suites').val());
});


$('#toggle-test-suite').click(function() {
    socket.emit('start', {suite: $('#test-suites').val()});
});
