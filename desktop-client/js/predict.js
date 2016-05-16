function render_temp(data) {
    var country_details = {'options':[]};
    $.each(data.teams, function(index, value) {
        country_details.options.push({'id': value[0], 'name': value[1], 'code': value[2]});
    });
    var html = Mustache.to_html(teams_template_1, country_details);
    $(html).appendTo('#teamlistcontainer1');
    var html = Mustache.to_html(teams_template_2, country_details);
    $(html).appendTo('#teamlistcontainer2');
    $('#country_list_1').on('change', function() {
        $("#teamlistcontainer2").empty();
        var html = Mustache.to_html(teams_template_2, country_details);
        $(html).appendTo('#teamlistcontainer2');
        $("#country_list_2 option[value="+this.value+"]").remove();
    });
    $('#country_list_2').on('change', function() {
        $("#teamlistcontainer1").empty();
        var html = Mustache.to_html(teams_template_1, country_details);
        $(html).appendTo('#teamlistcontainer1');
        $("#country_list_1 option[value="+this.value+"]").remove();
    });

}
var teams_template_1 = '<select class="form-control" style="width:200px; id="country_list_1">{{#options}}' +
                   '<option value="{{id}}">' +
                       '{{name}}' +
                   '</option>' +
               '{{/options}}</select>';

var teams_template_2 = '<select class="form-control" style="width:200px; id="country_list_2">{{#options}}' +
                  '<option value="{{id}}">' +
                      '{{name}}' +
                  '</option>' +
              '{{/options}}</select>';

$(document).ready(function () {
    $.get("http://127.0.0.1:5000/api/countries").done(function(data) {
        $("#spinnercontainer").remove();
        render_temp(data);
    });
});
