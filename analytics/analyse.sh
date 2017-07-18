#!/usr/bin/bash


for f in demo/*; do
  for g in $f/*; do
    res=`grep -ro app.intent $g | wc -l`
    echo "$g has $res app.intent sinks"
  done
done



