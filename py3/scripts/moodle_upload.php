<?php
    #if calling from this dir then ../../../../
    chdir("../../../");

    $username = $argv[1];
    $dice = $argv[2];
    $moodle_rootdir = getcwd();
    $moodle_clidir = $moodle_rootdir."/admin/cli/";
    $picdir =  $moodle_rootdir."/test/selenium/userpics/";
    $savedir = $moodle_rootdir."/test/selenium/screenshot/";
    /*$picdir =  $moodle_rootdir."/selenium/userpics/";
    $savedir = $moodle_rootdir."/selenium/screenshot/";*/
    $userdir = $savedir.$username."/";
    
    /*echo $moodle_rootdir.PHP_EOL;
    echo $moodle_clidir.PHP_EOL;
    echo $savedir.PHP_EOL;
    echo $userdir.PHP_EOL;
    echo $dice.PHP_EOL;
    echo $username;

    exit;*/

    copy($picdir.$dice.".jpeg", $userdir.$username.".jpeg");
    
    chdir($moodle_clidir);
    //echo getcwd();
    exec("php mv_updatepics.php --dir=$userdir --usr=$username", $output);
    print_r($output);
    //var_dump($output);

