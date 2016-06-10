var player0Ctr;
var player1Ctr;
var firstInn;
var secondInn;
var conditionFlag1 = 0;
var conditionFlag2 = 0;
var label = ["Top Order", "Top Middle Order", "Lower Middle Order","Tail End", "Spin","Fast"];
$('#backicon').click( function () {
    window.location.href = "index.html";
});

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

function displayData(countryValues, country1Id, country2Id, data){
  conditionFlag = 0;
  player0Ctr = 0;
  player1Ctr = 0;
  firstInn = [];
  secondInn = [];
  ctr = 0;
  $("#center_div").empty();
  $("#center_div").append($("<label><h4 style='color:#F8F8FF;margin-left:10px;width:200px;'>Select Players:</h4></label>"));
  $("#center_div").append($("<p style='color:#F8F8FF;margin-left:10px;width:200px;'><i>You must select atleast one wicketkeeper batsman among the players.</i></p>"));
  var index = 0
  var country = data.data;
  $("#center_div").append($("<li>"));
  $.each(country, function(x, player_details){
    console.log(ctr);
    $("<label><h5 style='color:#F8F8FF;margin-left:10px;width:200px;'><b>"+countryValues[ctr]+"</b></h5></label>").appendTo("#center_div");
    $("<div style='margin-left:30%;margin-right:30%' class='row playerlist"+ctr+"'>").appendTo("#center_div");
    $("<div style='width:100%' class='col-lg-6 "+countryValues[ctr].replace(' ', '')+"'>").appendTo(".playerlist"+ctr);
    $("<ul  class='list-group"+ctr+"'>").appendTo("."+countryValues[ctr].replace(' ', ''));
    $.each(player_details, function(y, player){
      $('<a />', {text: player[1] +" *"+player[2], href: '#/', class: "list-group-item player-order"+ctr, id: countryValues[ctr].replace(' ', '')+'_'+player[0]}).appendTo('.list-group'+ctr);
    });
    ctr++;
  });
  $("#center_div").append($("</li>"));
  $("<button id='predict-btn' class='btn btn-large btn-white'><b>Predict</b></button>").appendTo("#center_div")
  $("<button id='reset-btn' class='btn btn-large btn-white'><span class='glyphicon glyphicon-refresh'></span><b>Reset</b></button>").appendTo("#center_div");
}

$(document).on('click', '.player-order0', function () {
    var player_role = $("#"+this.id).text().split("*")[1];
    if (player_role == "Wicketkeeper batsman") {
        conditionFlag1 = 1;
    }
    $("#"+this.id).css("background-color","#888181");
    $("#"+this.id).text(++player0Ctr+"  "+$("#"+this.id).text());
    $("#"+this.id).css("pointer-events", "none");
    if(player0Ctr == 11) {
        $(".player-order0").css("pointer-events", "none");
    }
    firstInn.push(this.id.split('_')[1]);
  });

  $(document).on('click', '.player-order1', function () {
      var player_role = $("#"+this.id).text().split("*")[1];
      if (player_role == "Wicketkeeper batsman") {
          conditionFlag2 = 1;
      }
    $("#"+this.id).css("background-color","#888181");
    $("#"+this.id).text(++player1Ctr+"  "+$("#"+this.id).text());
    $("#"+this.id).css("pointer-events", "none");
    if(player1Ctr == 11) {
        $(".player-order1").css("pointer-events", "none");
    }
    secondInn.push(this.id.split('_')[1]);
  });

  $(document).on("click", "#predict-btn", function (){
      if (!conditionFlag1 || !conditionFlag2){
          alert("Choose atleast one wicketkeeper batsman.");
          window.location.href = "predict.html";
      }
      else {
          var finalOrder = [firstInn, secondInn];
          $.post("http://127.0.0.1:5000/api/results", JSON.stringify({"playerOrder": finalOrder}), function(data) {
            setting = data.setting;
            chasing = data.chasing;
      		strength = data.strength;
      		pos = [];
      		neg= [];
      		$.each(strength, function(x, s) {
      			if(s>0) {
      				pos.push(x);
      			}
      			else{
      				neg.push(x);
      			}
      		});
          $("#center_div").empty();
              $("#center_div").append($("<h2>Match Prediction Results:</h2>"));
              $("#center_div").append($("<p>Target Setting Win Percentage:</p><canvas id='canvas1' width='200' height='200'></canvas>\
              "));
              console.log(firstInn);
              var can = document.getElementById('canvas1');
              var context = can.getContext('2d');
              var text = Math.round(setting*100)+"%";
              var percentage = setting; // no specific length
              var degrees = percentage * 360.0;
              var radians = degrees * (Math.PI / 180);

              var x = 90;
              var y = 90;
              var r = 70;
              var s = 1.5 * Math.PI;

              context.beginPath();
              context.lineWidth = 5;
              context.arc(x, y, r, s, radians+s, false);
              context.strokeStyle="#39CE89";
              context.stroke();
              // context.closePath();
              context.font = "30px Arial";
              context.fillStyle = "white";
              context.fillText(text, 55, 100);
              context.textAlign="center";


              $("#center_div").append($("<p>Target Chasing Win Percentage:</p><canvas id='canvas2' width='200' height='200'></canvas>\
              "));
              var can = document.getElementById('canvas2');
              var context = can.getContext('2d');
              var text = Math.round(chasing*100)+"%";
              var percentage = chasing; // no specific length
              var degrees = percentage * 360.0;
              var radians = degrees * (Math.PI / 180);

              var x = 90;
              var y = 90;
              var r = 70;
              var s = 1.5 * Math.PI;

              context.beginPath();
              context.lineWidth = 5;
              context.arc(x, y, r, s, radians+s, false);
              context.strokeStyle="#39CE89";
              context.stroke();
              // context.closePath();
              context.font = "30px Arial";
              context.fillStyle = "white";
              context.fillText(text, 55, 100);
              context.textAlign="center";
              $("#center_div").append($("<div id='slot'></div>"));
              $("#slot").append($("<p><b>Slots Contributing to Win:</b></p>"));
      		  $.each(pos, function(x, p) {
        			$("#slot").append($("<p>"+label[p]+"</p>"));
      	      });
       		  $("#slot").append($("<p><b>Slots Witholding Win:</b></p>"));
      		  $.each(neg, function(x, p) {
        			$("#slot").append($("<p>"+label[p]+"</p>"));
      		  });
      });
  }
});

$("#selectplayers").click(function() {
    var country1Value = $("#country_list_1 :selected").text();
    var country2Value = $("#country_list_2 :selected").text();
    var country1ID = $("#country_list_1 :selected").val();
    var country2ID = $("#country_list_2 :selected").val();
    $.get('http://127.0.0.1:5000/api/players', { country1: country1Value, country2: country2Value})
    .done(function (data) {
        displayData([country1Value, country2Value], country1ID, country2ID, data);
    });
});
var teams_template_1 = '<select id="country_list_1">{{#options}}' +
                   '<option value="{{id}}">' +
                       '{{name}}' +
                   '</option>' +
               '{{/options}}</select>';

var teams_template_2 = '<select id="country_list_2">{{#options}}' +
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
