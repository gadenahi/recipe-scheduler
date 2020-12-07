var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
};


$(window).on("load", function() {
    var cat = getUrlParameter('category_id');
    var rec = getUrlParameter('recipe_id');

    if (cat === undefined) {
        cat = $('.new-recipe-category').val()
    }
    if (rec === undefined) {
        rec = $('.new-recipe').val()
    }

    var count_cat = $('.new-recipe-category').children().length
    for (var i=0; i<count_cat; i++) {
        var category = $('.new-recipe-category option:eq(' + i + ')');
//        console.log(category.attr('value'))
        if (category.attr('value') == cat) {
            category.prop('selected',true)
            }
        }

    var count = $('.new-recipe').children().length
    for (var i=0; i<count; i++) {
        var recipe = $('.new-recipe option:eq(' + i + ')');
        if (cat === recipe.attr('data-category')) {
            recipe.show();
//            console.log(recipe.attr('value'), rec)
            if (recipe.attr('value') == rec) {
                recipe.prop('selected',true)
            }
        } else {
            recipe.hide()
        }
    }
})


//$(document).ready(function() {
$(window).on("load", function() {
    var select_category = $('.new-recipe-category')

//    select_category.on('change', function(e){
//    select_category.change(function(){
    select_category.click(function(){

//        getUpdateSettings();
//        e.preventDefault();
        var count = $('.new-recipe').children().length
        for (var i=0; i<count; i++) {
            var recipe = $('.new-recipe option:eq(' + i + ')');
            if (select_category.val() === recipe.attr('data-category')) {
                recipe.show();
            } else {
                if (recipe.attr('data-category') === "0") {
                    recipe.show()
                    recipe.prop('selected',true)
                } else{
                    recipe.hide()
                }
            }
        }
    });

    // send the data of select box to analytics.html as filter_date
    function getUpdateSettings() {
        var send = {
            select_category: select_category.val()
        };
//        console.log("send", send)
        $.getJSON('./new_event', send, function(response) {
            console.log("response", response)
        })
    }
} );