#!/bin/bash

count=0

rm -rf test.txt

echo "Repo, URL, size (KB), intent functions"$'\r' >> test.txt


for f in demo-app/*; do
  for g in $f/*; do

    if [ -f $g/index.js ]
    then
	
	
	intent=`py -c "import alexa_analytics as a; a.find_intents(\"$g\")"`
	
	if [ "$intent" == 0 ]
	then
		miss=$(($miss+1))
		continue
		#intent=`grep -ro --exclude-dir=node_modules .intent $g | wc -l`
	fi
	   
	url="https://github.com/${g:9}"
	size=`du -shk $g --exclude=$g/.git --exclude=$g/node_modules`
	sizeRes=($size)

	#slots="grep -zPo "'slots':( |)(\{([^{}]++|(?1))*\})" $g/index.js"
	#echo $slots
	echo "${g:9} analytics:"
	echo "Repo size: ${sizeRes[0]}KB"
	echo "$intent intent functions"

	echo "${g:9}, $url, ${sizeRes[0]}, $intent"$'\r' >> test.txt
	echo "--------------------------------------------------------------"
	   
	count=$(($count+1))
    fi 
  done
done

echo "$count repos analysed."
echo "$miss repos could not be analysed."

#App.intent, const, https://, uri, Request, Request-promise, rp(options)


#find slots
#find destination URIs
#key modules used as sinks: i.e. request, request-promise, http, etc.
