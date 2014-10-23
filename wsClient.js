/* Added to the Header.php in the theme used by Wordpress
* within the <head>...</head> along with the lines below for the Popup
* <script src="jquery.min.js"></script> //jQuery library, stored in public_html
* <script src="jquery.bpopup.min.js"></script> //jQuery bPopup used for the notification pop up
*/
<script>
      $(function(){
        var ws;
        var logger = function(msg){
          var now = new Date();
          var sec = now.getSeconds();
          var min = now.getMinutes();
          var hr = now.getHours();
          $("#logger").html($("#logger").html() + "<br/>" + hr + ":" + min + ":" + sec + " ___ " +  msg);
          $('#logger').scrollTop($('#logger')[0].scrollHeight);
        }
 
        var sender = function() {
          var msg = $("#msg").val();
          if (msg.length > 0)
            ws.send(msg);
          $("#msg").val(msg);
        }
 
        ws = new WebSocket("ws://donationbox.commonslab.gr:8888/ws");
        ws.onmessage = function(evt) {
          logger(evt.data);
	   $('#element_to_pop_up').html('<span class="button b-close"><span>X</span></span><br>Thanks for donating <br>' + evt.data);
	   $('#element_to_pop_up').bPopup();
        };
        ws.onclose = function(evt) {
          $("#logger").text("Connection was closed...");
          $("#thebutton #msg").prop('disabled', true);
        };
        ws.onopen = function(evt) {
           $("#logger").text("Opening socket...");
        };
 
        $("#msg").keypress(function(event) {
          if (event.which == 13) {
             sender();
           }
        });
 
        $("#thebutton").click(function(){
          sender();
        });
      });
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
            loadUrl: 'popup.html' //Uses jQuery.load()
        });
</script>    
