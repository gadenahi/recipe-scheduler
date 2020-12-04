$(document).ready(function() {
    var select_group = $('#submit-form-group')

    select_group.on('change', function(){
        getUpdateSettings();

//        var value = $('input:radio[name="group_options"]:checked').val()
//        console.log(value)
//        localStorage.setItem("option", value);

        $("#submit-form-group").submit();

        // added to reload the png data
//        window.onload = reload;
    });


//    var itemValue = localStorage.getItem("option");
//    if (itemValue !== null) {
//        $("input[value=\""+itemValue+"\"]").click();
//        }


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