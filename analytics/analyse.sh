#!/bin/bash

count=0

for f in demo/*; do
  for g in $f/*; do
    res=`grep -ro app.intent $g | wc -l`
    echo "$g has $res app.intent sinks"
    count=$(($count+1))
  done
done

echo "$count repos analysed."

