#!/bin/bash

for i in {0..139} ; do

  fcrackzip -u -D -p ./words zip$i.zip >> pass.log

  echo "zip$i.zip" >> pass.log

done
