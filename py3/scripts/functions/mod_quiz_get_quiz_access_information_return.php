<?php
$resp = $curl->post($serverurl . $restformat, $params);
print prettyPrint($resp);