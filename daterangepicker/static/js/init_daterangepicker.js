$(document).ready(function() {
    function setDataRangeSelectedValue(selectControl) {
        var values = $(selectControl).val().split(' ');
        var select_id = $(selectControl).attr('id');
        var date_input_id_prefix = select_id.substr(0, select_id.length - 6);
        for(var i=0; i < values.length; i++) {
            if (values[i] != '-') {
                $('#' + date_input_id_prefix + i.toString()).val(values[i]);
            }
        }
    }

    $('.dateRangePicker')
    .show()
    .bind('change', function() {
        setDataRangeSelectedValue($(this));
    })
    .map(function() {
        setDataRangeSelectedValue($(this));
    });
    $('.dateRangePicker ~ input.vDateField').bind('change', function() {
         $(this).prevAll('select.dateRangePicker').val('- -');
    });
})