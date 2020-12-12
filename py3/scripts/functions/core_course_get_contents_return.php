<?php
$resp = $curl->post($serverurl . $restformat, $params);
print_r($resp);
$courseid = $argv[2];
//$file = getcwd()."/test/selenium/scripts/course_contents_$courseid.json";
$file = $moodle_rootdir."test/selenium/scripts/course_contents_$courseid.json";
$output = prettyPrint($resp);
saveOutput($file,$output,'w');
#print $output;

