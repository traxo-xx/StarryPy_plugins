function serverAction(text, url) {
    noty({
	  text: "Are you sure you want to " + text + "?",
	  layout: "center",
	  type: "warning",
	  buttons: [
	    {addClass: 'btn btn-primary', text: 'Ok', onClick: function($noty) {
	
	        $noty.close();
	        window.open(url, "_self");
	      }
	    },
	    {addClass: 'btn btn-danger', text: 'Cancel', onClick: function($noty) {
	        $noty.close();
	        noty({text: 'Action has been canceled.', layout: "center", type: 'success'});
	      }
	    }
	  ]
	});    
}

function playerAction(text, action) {
    noty({
	  text: "Are you sure you want to " + text + "?",
	  layout: "center",
	  type: "warning",
	  buttons: [
	    {addClass: 'btn btn-primary', text: 'Ok', onClick: function($noty) {
	
	        $noty.close();
	        window.open(url, "_self");
	      }
	    },
	    {addClass: 'btn btn-danger', text: 'Cancel', onClick: function($noty) {
	        $noty.close();
	        noty({text: 'Action has been canceled.', layout: "center", type: 'success'});
	      }
	    }
	  ]
	});    
}

function stopServer() {
    serverAction("stop the server", "/stopserver"); 
}

function restartServer() {
    serverAction("restart the server", "/restart"); 
}

function deletePlayer(player) {
    playerAction("delete the player " + player, "delete");
}

function twoDigits(n) {
    return n < 10 ? '0' + n : '' + n;
}