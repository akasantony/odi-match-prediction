$("document").ready(function (){
    $("#statsbtn").click(function () {
        var inngBatted = $("#inngbatted").val();
        var notOuts = $("#notouts").val();
        var runsScored = $("#runsscored").val();
        var ballsFaced = $("#ballsfaced").val();
        var fours = $("#fours").val();
        var sixes = $("#sixes").val();
        var hundreds = $("#hundreds").val();
        var fifties = $("#fifties").val();
        var highScores = $("#highscores").val();
        var inggBowled = $("#inngbowled").val();
        var ballsBowled = $("#ballsbowled").val();
        var runsConceded = $("#runsconceded").val();
        var wickets = $("#wickets").val();
        var maidens = $("#maidens").val();
        var fiveWickets = $("#fivewickets").val();
        // data = {"inngBatted": inngBatted, "notOuts": notOuts,
        // "runsScored": runsScored, "ballsFaced": ballsFaced, "fours": fours,
        // "sixes": sixes, "hundreds": hundreds, "fifties": fifties,
        // "highScores": highScores, "inggBowled": inggBowled, "ballsBowled": ballsBowled,
        // "runsConceded": runsConceded, "wickets": wickets, "maidens": maidens,
        // "fiveWickets": fiveWickets};
        // console.log(inngBatted);
        $.post('/stats', JSON.stringify({"inngBatted": inngBatted, "notOuts": notOuts,
        "runsScored": runsScored, "ballsFaced": ballsFaced, "fours": fours,
        "sixes": sixes, "hundreds": hundreds, "fifties": fifties,
        "highScores": highScores, "inggBowled": inggBowled, "ballsBowled": ballsBowled,
        "runsConceded": runsConceded, "wickets": wickets, "maidens": maidens,
        "fiveWickets": fiveWickets}), function(data) {
            alert("Sucessfully posted data.");
        });
    });
});
