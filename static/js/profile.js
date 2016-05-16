function display_sim_players(player_index) {
    $.post("/profile", JSON.stringify({"player_id": player_index}), function(data) {
        console.log(data);
        var points = []
        for(i=0; i<data.data.data.length;i++) {
            points.push({y: Math.round(data.data.data[i][0]*100)/100, legendText: data.data.data[i][1],
                label: data.data.data[i][2]});
        }
        console.log(points);
        var chart = new CanvasJS.Chart("chartContainer",
    	{
    		title:{
    			text: "Similarity Indexes:"
    		},
                    animationEnabled: true,
    		legend:{
    			verticalAlign: "center",
    			horizontalAlign: "left",
    			fontSize: 20,
    			fontFamily: "Helvetica"
    		},
    		theme: "theme2",
    		data: [
    		{
    			type: "pie",
    			indexLabelFontFamily: "Garamond",
    			indexLabelFontSize: 20,
    			indexLabel: "{label} {y}%",
    			startAngle:-20,
    			showInLegend: true,
    			toolTipContent:"{legendText} {y}%",
    			dataPoints: points
    		}
    		]
    	});
    	chart.render();
        $("#role").empty();
        $("#role").append($("<label><h3 style='color:#F8F8FF;margin-left:10px;width:200px;'>Preferred Roles:</h3></label>"));
        $("#role").append($("<p >Role 1: <h4 style='color: white;'><i>"+data.data.role[0][0]+"</i></h4></p>"));
        $("#role").append($("<p>Role 2: <h4 style='color: white;'><i>"+data.data.role[1][0]+"</i></h4></p>"));
});

}
$(document).ready(function () {
    $("#playername").keydown(function () {
        var qry = $("#playername").val()
        $.get( "/suggest", { data: qry} )
        .done(function(data){
            var x = data.data
            $( "#playername" ).autocomplete({
               source: data.data,
               select: function(event, ui) { display_sim_players(ui.item.indx); }
            });
        });
    });
});
