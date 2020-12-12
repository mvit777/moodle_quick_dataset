<?php
#core_webservice_get_site_info_return.php
$resp = $curl->post($serverurl . $restformat, $params);
print_r($resp);
echo PHP_EOL;
$file = getcwd()."/test/selenium/scripts/site_info.json";
$output = prettyPrint($resp);
saveOutput($file, $output, 'w');
