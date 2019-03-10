<?php

$c = 10;
$d = INF;
$a = hash("sha256", "a");
echo('echo($a);');
echo("\n");
echo($a);
echo("\n");
echo('echo($a**(0.5));');
echo("\n");
echo($a**(0.5));
echo("\n");
$a=(log10($a**(0.5)))**2;
echo($a);
echo($c*$c+$d*$d);
echo(INF == INF);

$c = "a";
echo("b" > "a");

?>