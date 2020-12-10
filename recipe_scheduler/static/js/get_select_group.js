$(document).ready(function() {
    var select_group = $('#submit-form-group')

    select_group.on('change', function(){
        getUpdateSettings();
        $("#submit-form-group").submit();

    });

    function reload() {
        location.reload()
    }

    // send the data of select box to analytics.html as filter_date
    function getUpdateSettings() {
        var send = {
            selected_group:$('input:radio[name="group_options"]:checked').val()
        };
        $.getJSON('./sub_menu', send, function(response) {
            console.log("response", response)
        })
    }
} );