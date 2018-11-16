$(document).ready(function() {
  var score = $('#score');
  var time_left = $('#time_left');

  function get_front_tiles() {
    var front_tiles = ""
    for (var j = 0; j < num_tiles; ++j) {
      var tile = document.getElementById(String(num_layers-1) + "-" + String(j))
      if (tile.style.backgroundColor == 'white') {
        front_tiles += "0"
      } else {
        front_tiles += "1"
      }
    }
    return front_tiles
  }

  $('.tap_tiles').click(function() {
    $.getJSON($SCRIPT_ROOT +'/check_game_ongoing',
      {id:parseInt($(this).attr('id'))},
      function(data) {
        if (data.ongoing == "true") {
          var front_tiles = get_front_tiles()
          var pressed_tiles = ""
          for (var j = 0; j < num_tiles; ++j) {
            if (j == data.id)
              pressed_tiles += "1"
            else
              pressed_tiles += "0"
          }

          if (front_tiles == pressed_tiles)
            window.location.href='/update_game';
  }});});

  function check_proper_tap() {
    $.getJSON($SCRIPT_ROOT +'/get_pressed_tiles',
      {},
      function(data) {
        var front_tiles = get_front_tiles()
        var pressed_tiles = data.pressed_tiles
        for (var j = 0; j < num_tiles; ++j) {
          var tile = document.getElementById(String(j))
          if (pressed_tiles.charAt(j) == "1")
            tile.style.backgroundColor = "DarkSlateGray"
          else
            tile.style.backgroundColor = "Gray"
        }

        //alert(front_tiles + "|" + pressed_tiles)
        if (front_tiles == pressed_tiles)
          window.location.href='/update_game';
  });}

  var frame_rate = 20
  function loop() {
    $.getJSON($SCRIPT_ROOT +'/check_game_ongoing',
      {},
      function(data) {
        if (data.ongoing == "true")
          check_proper_tap()
    });
    $.getJSON($SCRIPT_ROOT +'/get_score_data',
      {},
      function(data) {
        if (data.time_left <= 0) {
          window.location.href="/game_over/"+String(score.html());
        }
        score.html(data.score)
        time_left.html(parseFloat(data.time_left).toFixed(2))
    });
    setTimeout(loop, parseInt(1000/frame_rate));
  }
  var timer = setTimeout(loop, parseInt(1000/frame_rate))
});
