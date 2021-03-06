<?php
/**
 * The Header for our theme.
 *
 * Displays all of the <head> section and everything up till <div id="main">
 *
 * @package influence
 * @since influence 1.0
 * @license GPL 2.0
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
  <script src="/config.js"></script>
  <script src="/jquery.min.js"></script>
  <script src="/jquery.bpopup.min.js"></script>
  <script src="/video.js"> </script>
  <script src="/jquery.plugin.js"></script>
  <script src="/jquery.countdown.min.js"></script>
  <link href="/pro-bars.min.css" rel="stylesheet" type="text/css" media="all" />
  <link href="/video-js.css" rel="stylesheet" />
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<title><?php wp_title( '|', true, 'right' ); ?></title>
<style>

#element_to_pop_up, #success_to_pop_up, #error_to_pop_up, #thankyou_pop_up { display:none; color:#FFF;}
#element_to_pop_up, #success_to_pop_up, #error_to_pop_up, #thankyou_pop_up {
    min-height: 250px;
    background-color: #FFF;
    border-radius: 10px;
    box-shadow: 0px 0px 25px 5px #999;
    color: #111;
    display: none;
    min-width: 450px;
    padding: 25px;
}
.b-close, .bClose {
    background-color: #2B91AF;   
    border-radius: 7px;
    box-shadow: none;
    cursor: pointer;
    font: bold 131% sans-serif;
    padding: 0px 6px 2px;
    position: absolute;
    right: -7px;
    top: -7px;
}
#thankyou_pop_up {
  font-size: 24px;
}
.article.entry .entry-content {
padding-left: 20px;
padding-right: 20px;
}
#loading {
  position:absolute;
  margin-top: 10%;
  margin-left:30%;
  z-index: 99;
  display: none;
}
</style>
<script>
var ShowPopUps = true;
/*
 
function startTimer(duration, display) {
    var start = Date.now(),
        diff,
        minutes,
        seconds;
    function timer() {
        // get the number of seconds that have elapsed since 
        // startTimer() was called
        diff = duration - (((Date.now() - start) / 1000) | 0);

        // does the same job as parseInt truncates the float
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds; 

        if (diff <= 0) {
            // add one second so that the count down starts at the full duration
            // example 05:00 not 04:59
            start = Date.now() + 1000;
        }
    };
    // we don't want to wait a full second before the timer starts
    timer();
    setInterval(timer, 1000);
}
window.onload = function () {

    display = document.querySelector('#time');
    startTimer(10, display);
    setTimeout(function(){ document.location.href="/"; }, 10000)
};
*/
$(document).ready(function(){
    $("a").click(function(){
        $('#loading').show();
    });
});
  function SetTimer() {
        var oldDateObj = new Date();
        var newDateObj = new Date(oldDateObj.getTime() + 3*60000);
        $('#defaultCountdown').countdown({until: newDateObj, layout: '{mn} {snn}', expiryUrl: '/'});  
  }
  function ResetTimer() {
        var oldDateObj = new Date();
        var newDateObj = new Date(oldDateObj.getTime() + 3*60000);          
        $('#defaultCountdown').countdown('option',{until: newDateObj, layout: '{mn} {snn}', expiryUrl: '/'});  
  }
      $(function(){
        
        SetTimer();
        
        var ws;
        var donationdata;
        //Set progressbar
        var SetProgressBar = function() {
        sum = parseFloat($('#totalamount').html());
        goal = parseFloat($('#goal').html());
        percent = (sum/goal)*100;
        document.getElementById('probar').setAttribute("data-pro-bar-percent", String(percent));
        document.getElementById('probar').style.width = String(percent)+"%";
        $('#percentvalue').html(parseFloat(percent).toFixed(2)+"%");        
        }
        SetProgressBar();
        var logger = function(msg){
          var now = new Date();
          var sec = now.getSeconds();
          var min = now.getMinutes();
          var hr = now.getHours();
          $("#logger").html($("#logger").html() + "<br>" + hr + ":" + min + ":" + sec + " ___ " +  msg);
          $('#logger').scrollTop($('#logger')[0].scrollHeight);
        }
 
        var sender = function() {
          var msg = $("#msg").val();
          if (msg.length > 0)
            ws.send(msg);
          $("#msg").val(msg);
        }
        
        var donate = function() {
		//Validate Email & Name
        	name = document.getElementById('name').value
        	email = document.getElementById('email').value
var re = /[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
  if (email !='') {
		if (re.test(email) == false)
		{
   	  $('#email').css("background","#FF9999")
		}else{
		  $('#email').css("background","#99D699")
    }
  }
        	dpublic = document.getElementById('public').checked;
        	url = window.location.href
        	projectdetails = url.split('/');
		donationdata = $('#donationvalue_side').html()+$('#currency_side').html();
	//Send Donation Data to WebSocket Server
        	ws.send(name+"|"+email+"|"+dpublic+"|"+projectdetails[projectdetails.length-2]+"|"+projectdetails[projectdetails.length-1]+"|"+donationdata)
                //Add to total amount
		amount = parseFloat($('#totalamount').html());
		amount = parseFloat(amount)+parseFloat(donationdata);
                $('#totalamount').html(parseFloat(amount).toFixed(2))
		//clear form fields
document.getElementById('name').value = '';
document.getElementById('email').value = '';
                    $('#donationvalue_side').html(parseFloat(0).toFixed(2));
                    $('#donationvalue_pop').html(parseFloat(0).toFixed(2));
                    //Disable Donation button
$('#donationbutton').attr("disabled", "disabled");
//Redraw progress bar
        SetProgressBar();

        }
 
        ws = new WebSocket("ws://donationbox.pi:8888/ws");
        ws.onmessage = function(evt) {
            //logger(evt.data);
            if (evt.data == 'SUCCESS') {
              /*if (ShowPopUps) {
                $('#success_to_pop_up').bPopup();
              }  */
            } else if (String(evt.data).indexOf('|TOTAL|') > -1) {
                values = String(evt.data).split('|')
                //check PID
                $('#totalamount').html(parseFloat(values[3]).toFixed(2));
            } else if (evt.data == 'ERROR') {
              /*if (ShowPopUps) {
                $('#error_to_pop_up').bPopup();
              } */ 
            } else {
                donationdata = evt.data
                currency = String(evt.data).substring(String(evt.data).length - 3, String(evt.data).length)
                url = window.location.href
                //Single Project
                if (donationdata != "") {
                //Multi projects
                //if ((donationdata != "") && (url.indexOf('/project/') >= 0)) {
                    amount = parseFloat(donationdata);
                    if ($('#donationvalue_side').html().length > 0) {
                        amount += parseFloat($('#donationvalue_side').html())
                        $('#donationvalue_side').css("font-weight", "Bold");
                    }
                    $('#donationvalue_side').html(parseFloat(amount).toFixed(2));
                    $('#donationvalue_pop').html(parseFloat(amount).toFixed(2));                    
                    $('#currency_side').html(currency)
                    $('#currency_pop').html(currency)
		    $('#donationbutton').removeAttr("disabled");
                } else {
                    $('#donationvalue_pop').html('You have inserted ' + parseFloat(donationdata).toFixed(2) + '<br> but you must first select a project to donate that amount to...');
		    $('#donationbutton').attr("disabled", "disabled");
                }
            }
        };
        ws.onclose = function(evt) {
          $("#logger").text("Connection was closed...");
          //Disable Donation Button and make it red
          $('#donationbutton').attr("disabled", "disabled");          
          $('#donationbutton').css("color", "#CC2E2E");
        };
        ws.onopen = function(evt) {
           $("#logger").text("Opening socket...");
           $('#donationbutton').css("color", "#2ECC71");           
        };
 
        $("#msg").keypress(function(event) {
          if (event.which == 13) {
             sender();
           }
        });
        $("#donationbutton").click(function(){
          donate();
          if (ShowPopUps) {
            var bPopup = $('#thankyou_pop_up').bPopup();      
            setTimeout(function(){ document.location.href="/"; }, 3000)
          }  
        });
        $("#thebutton").click(function(){
          sender();
        });
      });
      $(document).scroll( function(){
        var oldDateObj = new Date();
        var newDateObj = new Date(oldDateObj.getTime() + 3*60000);          
        $('#defaultCountdown').countdown('option',{until: newDateObj, layout: '{mn} {snn}', expiryUrl: '/'});  
      });
      /*
      $(document).on("pagecreate",".single-post",function(){
        $(document).on("scrollstart",function(){
           ResetTimer();
        });                       
      });*/

      
</script>
<script>
    // $ is assigned to jQuery
    ;(function($) {    	
         // DOM Ready
        $(function() {
               
            // Binding a click event
            // From jQuery v.1.7.0 use .on() instead of .bind()
            $('#my-button').on('click', function(e) {
                // Prevents the default action to be triggered. 
                e.preventDefault();
                // Triggering bPopup when click event is fired
                $('#element_to_pop_up').bPopup();
            });
        });
    })(jQuery);
        $('element_to_pop_up').bPopup({
            contentContainer:'.content',
        });     
</script>   
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<div id="loading"><img src="/loading.gif" /></div>
	<?php
	$after_header = apply_filters('influence_after_header', '');

	if( empty($after_header) || !siteorigin_setting('home_menu_overlaps') ) {
		// We'll use a sentinel to take up space
		influence_site_header_sentinel();
		echo $after_header;
	}
	else {
		echo $after_header;
	}
	?>

	<div id="main" class="site-main">
  <div id="goal" style="display:none;">
    <?php $goal = get_post_meta( get_the_ID(), 'Goal', true ); 
      echo htmlspecialchars($goal);
    ?>
  </div>
