/**
 * Scrolls calendar view to today.
 */
function go_today() {
    if ($('#calendar').length) {
        $('html, body').animate({
            scrollTop: $("#today").offset().top - 150
        }, 200);
    }
}

/**
 * Scrolls calendar view to selected day.
 */
function go_day() {   
    $("#calendar-datepicker").change(function () {

        var day_raw = $("#calendar-datepicker").val().split(/-/);
        var day_to_go = day_raw[2] + "-" + day_raw[1] + "-" + day_raw[0];

        $('html, body').animate({
            scrollTop: $("div.day-tag:contains(\'" + day_to_go + "\')").offset().top - 150
        }, 200);
    })    
}


/**
 * Meal color_picker click event.
 */
function color_picker() {

    var bg_custom = [
        'bg-custom-red',
        'bg-custom-orange',
        'bg-custom-aquamarina',
        'bg-custom-aqua',
        'bg-custom-softviolet',
        'bg-custom-grey',
        'bg-custom-pink',
        'bg-custom-yellow',
        'bg-custom-green',
        'bg-custom-blue',
        'bg-custom-purple',
        'bg-custom-white'
    ];

    $(bg_custom).each(function (index) {
        $('.' + bg_custom[index]).click(function () {
            // Meal name field background color
            $('#item-preview').removeClass();
            $('#item-preview').addClass('form-control');
            $('#item-preview').addClass(bg_custom[index] + ' text-white');
            if (bg_custom[index] == 'bg-custom-white') {
                $('#item-preview').removeClass('text-white');
            }

            // Save background class to hidden input
            $('#bg-color').val(bg_custom[index]);
        });
    });
}


/**
 * Menu meal_picker behaviour.
 */
function meal_picker() {

    $('#meal-picker').change(function () {
        // This part controls background color
        var bg_color_class = $(this).val();
        $('#meal-picker').removeClass();
        $('#meal-picker').addClass('form-control');
        $('#meal-picker').addClass(bg_color_class);
        $('#meal-picker').addClass('text-white');
        if (bg_color_class == 'bg-custom-white') {
            $('#meal-picker').removeClass('text-white');
        }
        
        // This part prepare meal id to be retrieved by logic
        $('#meal-id').val($('#meal-picker option:selected').text())
    });
}


/**
 * Updates delete_date on page loading
 */
function delete_date_onload() {
    $('.delete-date').val($('#date').val());
}


/**
 * Redirects to selected day menu card
 */
function date_redirect() {   
    $('#date').change(function () {
        date_raw = $('#date').val();
        date_array = date_raw.split('-');
        new_url = '/menu/card/' + date_array[0] + '/' + date_array[1] + '/' + date_array[2];
        document.location.href = new_url;
    });
}


/***
 * Adds auto-closing to bootstrap alerts
 */
function auto_close_alert() {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}


/**
 * Changes collapse button text on cards
 */
function collapse_button_text() {
    $("[data-toggle='collapse']").click(function() {
        txt = $(this).text();
        if (txt.indexOf("Mostrar") > -1) {
            $(this).text(txt.replace("Mostrar", "Ocultar"));
        } else if (txt.indexOf("Ocultar") > -1) {
            $(this).text(txt.replace("Ocultar", "Mostrar"));
        }
    });
}

/**
 * Set min, max and val of navbar datepicker
 */
function set_datepicker() {
    
    var date_raw = new Date();
    var date_today = date_raw.toISOString().substring(0, 10);

    date_raw.setDate(date_raw.getDate() - 365);
    var date_min = date_raw.toISOString().substring(0, 10);

    date_raw.setDate(date_raw.getDate() + 365*2);
    var date_max = date_raw.toISOString().substring(0, 10);

    $("#calendar-datepicker").val(date_today);
    $("#calendar-datepicker").attr('min', date_min);
    $("#calendar-datepicker").attr('max', date_max);    
}


/**
 * Controls 'active section' behaviours
 */
function active_section() {
    if ($('#calendar').length) {
        $('.navbar-nav li:eq(0)').addClass('active');
        $('#calendar-date-picker').removeClass('d-none');
        set_datepicker();
        go_today();
        go_day();
    }

    else if ($('#menu-card').length) {
        $('.navbar-nav li:eq(1)').addClass('active');
        collapse_button_text()
        meal_picker();
        delete_date_onload();
        date_redirect();        
    }

    else if ($('#meal-card').length) {
        $('.navbar-nav li:eq(2)').addClass('active');
        collapse_button_text()
        color_picker();
    }

    else if ($('#dish-card').length) {
        $('.navbar-nav li:eq(3)').addClass('active');
        collapse_button_text()
    }

}


/**********************************************************************************
 * JQuery Document Ready
 */
$(document).ready(function () {
    active_section();
    window.setTimeout(auto_close_alert, 5000);   
});