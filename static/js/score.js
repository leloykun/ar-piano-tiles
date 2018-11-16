$(document).ready(function() {
  var score = $('#score');
  var time_left = $('#time_left');

  var frame_rate = 20
  function score_loop() {
    $.getJSON($SCRIPT_ROOT +'/get_score_data',
      {},
      function(data) {
        if (data.time_left <= 0) {
          window.location.href="/game_over/"+String(score.html());
        }
        score.html(data.score)
        time_left.html(parseFloat(data.time_left).toFixed(2))
    });
    setTimeout(score_loop, parseInt(1000/frame_rate));
  }
  var timer = setTimeout(score_loop, parseInt(1000/frame_rate))
});
