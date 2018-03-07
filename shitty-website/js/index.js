// PRESS THE MENU BUTTON TO TRIGGER ANIMATION
// PRESS PLAY BUTTON TO LISTEN THE DEMO SONG

// As seen on: "https://dribbble.com/shots/2144866-Day-5-Music-Player-Rebound/"

// THANK YOU!

// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("get_playlists");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
var audio = document.getElementById('audio');
var playpause = document.getElementById("play");

$(function(){
	$('form').on('submit', function(event)
	{
		$.ajax({data: {
			username : $('#username').val(),
			password : $('#password').val(),
			platform : $('#platform').val()
		},
		type : 'POST',
		url : '/getPlaylists'
		});
	});
});

function togglePlayPause() {
   if (audio.paused || audio.ended) {
      playpause.title = "Pause";
      audio.play();
   } else {
      playpause.title = "Play";
      audio.pause();
   }
}

// When the user clicks on the button, open the modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}