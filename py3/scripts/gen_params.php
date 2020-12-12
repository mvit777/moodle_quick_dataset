<?php

// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Web services automatic generation of required array structure
 * for Soap calls in PHP 
 * 
 * 
 * usage on the command line php gen_php_soap_args_code.php >nameofphpfile.php 
 *
 * @package   webservice
 * @copyright 2011 Moodle Pty Ltd (http://moodle.com)
 * @license   http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 * @author Patrick Pollet
 */

define('CLI_SCRIPT', true);
/**
 * must be copied in some directory under local/ 
 * otherwise adjust the relative path to config.php 
 */
require_once('../../../config.php');
require($CFG->dirroot . '/webservice/lib.php');


 //collect all available defines for VALUE_  and PARAM_
        $VALUES = array();
        $PARAMS=array();

        $consts = get_defined_constants (true);
       // print_r($consts);
        foreach ($consts['user'] as $key => $value) {
            if (substr ($key, 0, 6) == 'VALUE_') {
                $VALUES[$value] = $key;
            }else if (substr ($key, 0, 6) == 'PARAM_') {
                $PARAMS[$value] = $key;
                
            }
        }

//print_r($VALUES);
//print_r($PARAMS);
//die();

// get all the function descriptions
$functions = $DB->get_records('external_functions', array(), 'name');
$functiondescs = array();

   print ("<?php\n");
   $n=0;
foreach ($functions as $function) {
    $functionname=$function->name;
    //if (substr($functionname,0,6)=="oktech")
    //    continue;
    $functiondesc = external_api::external_function_info($function);
    //print_r($functiondesc);
    print ("// $functionname\n");
    print ("\$args$n=");
    parse_parameters($functiondesc->parameters_desc,1);
    print (';');
    print ("\nprint_r(\$args$n);\n\n\n");
    $n++;
}


/**
 * recursive function printing out a parameter description
 * suitable for usage are the second argument of the WS call
 * by $client->__soapCall($functionname, $args); 
 * @param  $description
 * @param int  $indent
 */

function parse_parameters ($description,$indent) {
    global $VALUES,$PARAMS;
    //print_r($description);
     $comma =$indent>1 ? ',':'';
    if ($description instanceof external_value) {
        print do_indent($indent).sample_value_of ($description->type).$comma;
        print " //\t\t{$PARAMS[$description->type]}\t{$VALUES[$description->required]}\t[$description->default]\n";
        //print_r($description);

    } else if ($description instanceof external_single_structure) {
        print  do_indent($indent).("array (   //e_s_s \n");
        foreach ($description->keys as $key=>$subdesc) {
            print do_indent($indent).("'$key' =>");
            parse_parameters($subdesc,$indent+1);
            //print do_indent($indent).(",\n");
        }
     
        print do_indent($indent).(")$comma\n");
        
    } else if ($description instanceof external_multiple_structure) {
        print  do_indent($indent).("array(  // e_m_s\n");
        parse_parameters($description->content, $indent+1);
        print do_indent($indent).(" )$comma\n");


    } else {
        throw new invalid_parameter_exception('Invalid external api description');
    }

}

/**
 * add nb tabulations 
 * @param int $nb
 * @return a string with nb tabulations
 */
function do_indent ($nb) {
   $ret='';
   for ($i=0; $i<$nb;$i++)
       $ret.="\t";
   return $ret;        
}

/**
 * return a sample value for a Moodle type 
 * Enter description here ...
 * @param unknown_type $type
 */
function sample_value_of ($type) {
    if ($type==PARAM_INTEGER || $type==PARAM_NUMBER)
           return "1";
     else if ($type==PARAM_FLOAT)
             return '1.1';
     else if ($type==PARAM_BOOL)
         return 'true';
     else return ("''");          
}

/*$token = '689576fcf39bf3e8c3b47d7c54fea26d';
$domainname = 'http://moodle36.localhost/';
//$functionname = 'core_webservice_get_site_info';
$functionname = 'core_files_upload';
$serverurl = $domainname . '/webservice/rest/server.php'. '?wstoken=' . $token . '&wsfunction='.$functionname;
//$client = new JsonClient($serverurl);
//$resp = $client->__jsonCall($functionname, $args);*/