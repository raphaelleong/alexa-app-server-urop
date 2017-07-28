#!/bin/bash

count=0

rm -rf test.txt

echo "Repo, URL, size (KB), intent functions"$'\r' >> test.txt


for f in demo-app/*; do
  for g in $f/*; do

    if [ -f $g/index.js ]; then
    	echo "${g:9} analytics:"
	res=`grep -ro --exclude-dir=node_modules .intent $g | wc -l`
	   
	url="https://github.com/${g:9}"
	size=`du -shk $g --exclude=$g/.git --exclude=$g/node_modules`
	sizeRes=($size)

	#slots="grep -zPo "'slots':( |)(\{([^{}]++|(?1))*\})" $g/index.js"

	#echo $slots
	echo "Repo size: ${sizeRes[0]}KB"
	echo "$res intent function sinks"

	echo "${g:9}, $url, ${sizeRes[0]}, $res"$'\r' >> test.txt
	echo "--------------------------------------------------------------"
	   
	count=$(($count+1))
    fi 
  done
done

echo "$count repos analysed."

#App.intent, const, https://, uri, Request, Request-promise, rp(options)


#find slots
#find destination URIs

