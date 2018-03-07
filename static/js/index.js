// PRESS THE MENU BUTTON TO TRIGGER ANIMATION
// PRESS PLAY BUTTON TO LISTEN THE DEMO SONG

// As seen on: "https://dribbble.com/shots/2144866-Day-5-Music-Player-Rebound/"

// THANK YOU!

// Get the modal
var modal = document.getElementById('myModal');

var gusername;
var susername;
var gpassword;
var spassword;
var currentGPlaylist;
var currentSPlaylist;

// Get the button that opens the modal
var btn = document.getElementById("login");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var audio = document.getElementById('audio');
var playpause = document.getElementById("play");

$(function(){
	$(":radio").click(function() {
		credit = $(":radio[name=platform]:checked");
		console.log($(this).val() + " - " + $(this).is(":checked"));
	});
	
	$('#playlist_form').on('submit', function(event)
	{
		var user;
		var pass;
		if($(":radio[name=platform2]:checked").val() == "spotify")
		{
			user = susername
			pass = spassword
		}
		else
		{
			user = gusername
			pass = gpassword
		}
		var a = $(":radio[name=platform2]:checked").val()
		var aj = {dataType: "json", async:false, data: {
			username : user,
			password : pass,
			platform : a
		},
		type : 'POST',
		url : '/getPlaylists',
		};
		console.log(aj)
		event.preventDefault();
		$.ajax(aj).done(function(data)
		{
			console.log(data)
			var str = "";
			$.each(data.playlists, function(k, v) {
				str += "<tr class=\"song\">"
				str += "<td class=\"title\"><h6>"+v+"</h6></td>"
				str += "</tr>"
			});
			$('#song_list').html(str);
		}).fail(function(xhr, status, error){
			alert(xhr.responseText + status + error)
			console.log('broke')
		}).always(function(){console.log('always')
		});
	});
	
	$('#login_form').on('submit', function(event)
	{
		event.preventDefault();
		if($(":radio[name=platform1]:checked").val() == "spotify")
		{
			susername = $('#username').val()
			spassword = $('#password').val()
		}
		else
		{
			gusername = $('#username').val()
			gpassword = $('#password').val()
		}
	});
	
	$('#loadsong_form').on('submit', function(event)
	{
		var user;
		var pass;
		var a = $(":radio[name=platform3]:checked").val()
		if($(":radio[name=platform3]:checked").val() == "spotify")
		{
			user = susername
			pass = spassword
			currentSPlaylist = $('#playlist').val();
		}
		else
		{
			user = gusername
			pass = gpassword
			currentGPlaylist = $('#playlist').val();
		}
		var aj = {dataType: "json", async:false, data: {
			username : user,
			password : pass,
			platform : a,
			playlistName : $('#playlist').val()
		},
		type : 'POST',
		url : '/loadSongs',
		};
		console.log(aj)
		event.preventDefault();
		$.ajax(aj).done(function(data)
		{
			console.log(data)
			var str = "";
			$.each(data.songs, function(k, v) {
				str += "<tr class=\"song\">"
				str += "<td class=\"title\"><h6>"+v+"</h6></td>"
				str += "</tr>"
			});
			$('#playlist-info').html("<h4>"+"Currently editting: "+$('#playlist').val()+"</h4>")
			$('#song_list').html(str);
		}).fail(function(xhr, status, error){
			alert(xhr.responseText + status + error)
			console.log('broke')
		}).always(function(){console.log('always')
		});
	});
	
	$('#search_form').on('submit', function(event)
	{
		var a = $(":radio[name=platform]:checked").val()
		var aj = {dataType: "json", async:false, data: {
			songName: $('#search_bar').val(),
			susername : susername == null ? "" : susername,
			spassword : spassword == null ? "" : spassword,
			gusername : gusername == null ? "" : gusername,
			gpassword : gpassword == null ? "" : gpassword
		},
		type : 'POST',
		url : '/search',
		};
		console.log(aj)
		event.preventDefault();
		$.ajax(aj).done(function(data)
		{
			console.log(data)
			var str = "";
			$.each(data.songs, function(k, v) {
				str += "<tr class=\"song\">"
				str += "<td class=\"title\"><h6>"+v['track']+"</h6></td>"
				str += "<td class=\"title\"><h6>"+v['platform']+"</h6></td>"
				str += "<td class=\"title\"><h6><a id=\"add\" href=\"#\" onclick=\"add(\'"+v['track']+"\',\'"+v['platform']+"\')\">Add</h6></a></td>"
				str += "<td class=\"title\"><h6><a id=\"remove\" href=\"#\" onclick=\"remove(\'" + v['track'] + "\',\'" + v['platform'] + "\')\">Remove(if exists)</h6></a></td>"
				str += "</tr>"
			});
			$('#song_list').html(str);
		}).fail(function(xhr, status, error){
			alert(xhr.responseText + status + error)
			console.log('broke')
		}).always(function(){console.log('always')
		});
		
		
	});
});

function add(track, platform)
{
	var user;
	var pass;
	var playlist;
	if(platform == "spotify")
	{
		user = susername
		pass = spassword
		playlist = currentSPlaylist
	}
	else
	{
		user = gusername
		pass = gpassword
		playlist = currentGPlaylist
	}
	var aj = {dataType: "json", async:false, data: {
		username : user,
		password : pass,
		platform : platform,
		playlist : playlist,
		track : track
	},
	type : 'POST',
	url : '/add',
	};
	console.log(aj)
	event.preventDefault();
	$.ajax(aj)
}

function remove(track, platform)
{
	var user;
	var pass;
	var playlist;
	if(platform == "spotify")
	{
		user = susername
		pass = spassword
		playlist = currentSPlaylist
	}
	else
	{
		user = gusername
		pass = gpassword
		playlist = currentGPlaylist
	}
	var aj = {dataType: "json", async:false, data: {
		username : user,
		password : pass,
		platform : platform,
		playlist : playlist,
		track : track
	},
	type : 'POST',
	url : '/remove',
	};
	console.log(aj)
	event.preventDefault();
	$.ajax(aj)
}

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

var modal2 = document.getElementById('myModal2');
var btn2 = document.getElementById("get_playlists");
var span2 = document.getElementsByClassName("close")[1];

// When the user clicks on the button, open the modal 
btn2.onclick = function() {
    modal2.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span2.onclick = function() {
    modal2.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
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

var modal3 = document.getElementById('myModal3');
var btn3 = document.getElementById("load_songs");
var span3 = document.getElementsByClassName("close")[2];

// When the user clicks on the button, open the modal 
btn3.onclick = function() {
    modal3.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span3.onclick = function() {
    modal3.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal3) {
        modal3.style.display = "none";
    }
}