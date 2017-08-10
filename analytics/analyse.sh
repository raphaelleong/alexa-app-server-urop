#!/bin/bash

count=0

rm -rf test.txt
echo "Repo, URL, size (KB), intent functions, slots, data sink module, sinks found"$'\r' >> analyse_results.txt
declare -a moduleCount=(0 0 0)

for f in demo-app/*; do
  for g in $f/*; do
    if [ -f $g/index.js ]
    then
	index=0
	url="https://github.com/${g:9}"
	intent=`py -c "import alexa_analytics as a; a.find_intents(\"$g\")"`
	if [ "$intent" == 0 ]
	then
		miss=$(($miss+1))
		continue
		#intent=`grep -ro --exclude-dir=node_modules .intent $g | wc -l`
	fi
	   
	size=`du -shk $g --exclude=$g/.git --exclude=$g/node_modules`
	sizeRes=($size)

	slots=`py -c "import alexa_analytics as a; a.find_slots(\"$g\")"`
	if [ "$slots" == -1 ]
	then
		miss=$(($miss+1))
		continue
	fi
	

	declare -a moduleSearch=("request" "request-promise") 

	module="n/a"
	moduleRes="n/a"
	for i in "${moduleSearch[@]}"
	do
		moduleFile=`py -c "import alexa_analytics as a; a.find_module_file(\"$g\", \"$i\")"`
		if [ "$moduleFile" != -1 ]
		then
			moduleRes="$i"
			moduleCount[$index]=$((${moduleCount[$index]}+1))
			break
		fi
		index=$(($index+1))
	done

	if [ "$index" == 0 ]
	then
		module=`py -c "import alexa_analytics as a; a.find_req_sinks(\"$g/$moduleFile\")"`
	fi
	if [ "$index" == 1 ]
	then
		module=`py -c "import alexa_analytics as a; a.find_rp_sinks(\"$g/$moduleFile\")"`
	fi
	if [ "$index" == 2 ]
	then
		moduleCount[$index]=$((${moduleCount[$index]}+1))
	fi


	echo "${g:9} analytics:"
	echo "Repo size: ${sizeRes[0]}KB"
	echo "No. of intents: $intent"
	echo "No. of Slots: $slots"
	echo "Data sink module: $moduleRes"
	echo "No. of sinks: $module"
	
	echo "${g:9}, $url, ${sizeRes[0]}, $intent, $slots, $moduleRes, $module"$'\r' >> analyse_results.txt
	echo "--------------------------------------------------------------"
	   
	count=$(($count+1))


	slotGraph="$slotGraph, $slots"

	if [ "$module" != n/a ] 
	then
		sinkGraph="$sinkGraph, $module"
	fi
	intentGraph="$intentGraph, $intent"
    fi 
  done
done

echo "$count repos analysed."
echo "$miss repos could not be analysed."

echo "request: ${moduleCount[0]}"
echo "request-promise: ${moduleCount[1]}"
echo "others/local server: ${moduleCount[2]}"

graph=`py -c "import plot; plot.draw_hist([${slotGraph:1}],[${sinkGraph:1}],[${intentGraph:1}])"`
echo "$graph"

#App.intent, const, https://, uri, Request, Request-promise, rp(options)


#find slots
#find destination URIs
#key modules used as sinks: i.e. request, request-promise, http, etc.
