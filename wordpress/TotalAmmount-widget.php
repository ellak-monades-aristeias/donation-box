<style>
.widgets {
  background: #fbfbfb;
  -webkit-box-shadow: 0 1px 3px rgba(0,0,0,0.175);
  -moz-box-shadow: 0 1px 3px rgba(0,0,0,0.175);
  box-shadow: 0 1px 3px rgba(0,0,0,0.175);
  padding: 25px;
position:fixed;
}
#totalamount {
color: black;
font-weight: bold;
float:left;
}
#currency {
font-size: 14px;
font-weight: normal;
color: #666;
display: inline;
}
</style>
<div class="totalamountwidget"><div id="totalamount" >
<?php 
$conn = new mysqli("localhost", "root", "c0mm0ns", "wordpress");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
setlocale(LC_MONETARY, 'el_GR');
$pid = get_the_ID();
$sql = "SELECT SUM(Ammount) FROM donations WHERE ProjectID=$pid";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
$sum = $row['SUM(Ammount)'];
print money_format('%.2n', $sum);
    }
} else {
    print "0";
}
$conn->close();
?>
</div>
<div id="currency">&nbsp;EUR</div>
</div>
<div style="display: block;">RAISED OF <?php $goal = get_post_custom_values( 'Goal' ); print $goal[0]; ?>&euro; GOAL</div>
