$(document).ready(function () {
    $("#updatebtn").click( function() {
        var player_name = $("#name").val();
        var country = $("#country").val();
        var playerrole = $( "#playerrole" ).val();
        var battingrole = $("#battingrole").val();
        var bowlingrole = $("#bowlingrole").val();

        $.post('/update', JSON.stringify({"name": player_name, "country": country,
            "playerrole": playerrole, "battingrole": battingrole, "bowlingrole": bowlingrole}), function(data){
                if (data.data == '200') {
                    window.location.href = "/stats";
                }
            });
    });
});
