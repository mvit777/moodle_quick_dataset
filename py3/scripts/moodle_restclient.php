<?php
/**
 * REST client for Moodle 2
 * Return JSON or XML format
 *
 * @authorr Jerome Mouneyrac
 */

 #if calling from this dir then ../../../
 $original_dir = getcwd()."/";
 
 if(strstr($original_dir, "/scripts/")):
    chdir("../../../");
 else:
    chdir("../../");
    $original_dir = $original_dir."scripts/";
 endif;
 
 require_once($original_dir.'helpers/general.php');
 $moodle_rootdir = getcwd();
 if(strstr($moodle_rootdir,"/test")):
   $moodle_rootdir = substr($moodle_rootdir,0, strpos($moodle_rootdir, 'test'));
 endif;

/// SETUP - NEED TO BE CHANGED
$token = '689576fcf39bf3e8c3b47d7c54fea26d';
$domainname = 'http://moodle36.localhost/';
$functiondir = $original_dir."functions/";
$functionname = $argv[1];
$functionparams = $functiondir.$functionname."_params.php";
$functionreturn = $functiondir.$functionname."_return.php";

// REST RETURNED VALUES FORMAT
$restformat = 'json'; //Also possible in Moodle 2.2 and later: 'json'
                     //Setting it to 'json' will fail all calls on earlier Moodle version

/// REST CALL
header('Content-Type: text/plain');
/// PARAMETERS - NEED TO BE CHANGED IF YOU CALL A DIFFERENT FUNCTION
require_once($functionparams);

$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
require_once($original_dir.'curl.php');
$curl = new curl;
//if rest format == 'xml', then we do not add the param for backward compatibility with Moodle < 2.2
$restformat = ($restformat == 'json')?'&moodlewsrestformat=' . $restformat:'';
require_once($functionreturn);
//$resp = $curl->post($serverurl . $restformat, $params);
//print_r($resp);
//$resp = json_decode($resp);
//print_r($resp);
