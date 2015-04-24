<div id="daysleft" style="padding-bottom:15px;margin-bottom:15px;border-bottom:1px solid #ccc;">&nbsp;
<?php 
$days = get_post_custom_values( 'Finish Date' ); 
if ($days[0] > 0) {
$now = time(); // or your date as well
$date = strtotime($days[0]);
$datediff = $now - $date;
echo floor(-$datediff/(60*60*24));
print '&nbsp;days left';
}
?></div>
