<?php
#enrol_manual_enrol_user_return
$resp = $curl->post($serverurl . $restformat, $params);
if($resp=='null'):
    print "user enrolled".PHP_EOL;
else:
    print prettyPrint($resp);
endif;
