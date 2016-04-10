function displayData(countryValues, country1Id, country2Id, data){
  player0Ctr = 0;
  player1Ctr = 0;
  firstInn = [];
  secondInn = [];
  $(".center_div").empty();
  $(".center_div").append($("<label><h4 style='color:#F8F8FF;margin-left:10px;width:200px;'>Select Players:</h4></label>"));
  var index = 0
  var country = data.data;
  $(".center_div").append($("<li>"));
  $.each(country, function(x, player_details){
    $("<label><h5 style='color:#F8F8FF;margin-left:10px;width:200px;'><b>"+countryValues[x]+"</b></h5></label>").appendTo(".center_div");
    $("<div style='margin-left:30%;margin-right:30%' class='row playerlist"+x+"'>").appendTo(".center_div");
    $("<div style='width:100%' class='col-lg-6 "+countryValues[x]+"'>").appendTo(".playerlist"+x);
    $("<ul  class='list-group"+x+"'>").appendTo("."+countryValues[x]);
    console.log(x);
    $.each(player_details, function(y, player){
      $('<a />', {text: player[1], href: '#/', class: "list-group-item player-order"+x, id: countryValues[x]+'_'+player[0]}).appendTo('.list-group'+x)
    });
  });
  $(".center_div").append($("</li>"));
  $("<a id='predict-btn' class='btn btn-large btn-white'><b>Predict</b></a>").appendTo(".center_div")
  $("<a id='reset-btn' class='btn btn-large btn-white'><span class='glyphicon glyphicon-refresh'></span><b>Reset</b></a>").appendTo(".center_div");
}
var player0Ctr = 0;
var player1Ctr = 0;
var firstInn = [];
var secondInn = [];
var country1Id;
var country2Id;
var country1Value;
var country2Value;
var plaeyerData;

$(document).ready(function () {
  $('#player').click(function () {
    country1Id = $( "#country1" ).val();
    country2Id = $( "#country2" ).val();
    country1Value = $( "#country1 option:selected" ).text();
    country2Value = $( "#country2 option:selected" ).text();
    $.get( "/getplayers", { country1Id: country1Id, country2Id: country2Id} )
    .done(function(data){
      plaeyerData = data;
      displayData([country1Value, country2Value], country1Id, country2Id, plaeyerData)
    });
  });

  $(document).on('click', '.player-order0', function () {
    $("#"+this.id).css("background-color","#888181");
    $("#"+this.id).text(++player0Ctr+"  "+$("#"+this.id).text());
    $("#"+this.id).css("pointer-events", "none");
    firstInn.push(this.id.split('_')[1]);
  });

  $(document).on('click', '.player-order1', function () {
    $("#"+this.id).css("background-color","#888181");
    $("#"+this.id).text(++player1Ctr+"  "+$("#"+this.id).text());
    $("#"+this.id).css("pointer-events", "none");
    secondInn.push(this.id.split('_')[1]);
  });

  $(document).on("click", "#predict-btn", function (){
    var finalOrder = $.merge(firstInn, secondInn);
    $.post("/predict", JSON.stringify({"playerOrder": finalOrder}), function(data) {
        if (data.country_1 > data.country_2){
            prob = data.country_1
            console.log(prob);
            value = country1Value;
        }
        else {
            prob = data.country_2
            value = country2Value;
        }
        $("#title").text("Match prediction results:")
        $(".center_div").empty();
        $(".center_div").append($("<div class='flag-wrapper'>\
              <div class='img-thumbnail flag flag-icon-background flag-icon-in'></div>\
              <p>"+value+"</p>\
            </div></div><canvas id='canvas1' width='200' height='200'></canvas>\
        "));
        var can = document.getElementById('canvas1');
        var context = can.getContext('2d');
        var text = Math.round(prob*100)+"%";
        var percentage = prob; // no specific length
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
    });
    console.log(finalOrder);
  });

  $(document).on("click", "#reset-btn", function (){
    displayData([country1Value, country2Value], country1Id, country2Id, plaeyerData);
    });
});