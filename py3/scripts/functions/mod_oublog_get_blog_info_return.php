<?php
#mod_oublog_get_blog_info_params_return
$resp = $curl->post($serverurl . $restformat, $params);
print prettyPrint($resp);