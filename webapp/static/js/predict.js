function displayData(country1Value, country2Value, country1Id, country2Id, data){
  $(".center_div").empty();
    $(".center_div").append("<label><h4 style='color:#F8F8FF;margin-left:10px;width:200px;'>Select Players:</h4></label>");
    $(".center_div").append("<label><h5 style='color:#F8F8FF;margin-left:10px;width:200px;'>"+country1Value+"</h5></label>");


}

$(document).ready(function () {
    $('#player').click(function () {
      country1Id = $( "#country1" ).val();
      country2Id = $( "#country2" ).val();
      country1Value = $( "#country2" ).text();
      country2Value = $( "#country2" ).text();
      $.get( "/getplayers", { country1Id: country1Id, country2Id: country2Id} )
      .done(function(data){
        displayData(country1Value, country2Value, country1Id, country2Id, data)
      });
    });
})
