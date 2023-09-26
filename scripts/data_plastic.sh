#!/bin/bash

filename=`basename $1`
YearMonth=${filename%%_*}
if [[ $YearMonth -lt 202303 && $YearMonth -ne 202211 ]]; then
	unzip -p $1 | \
		awk -F" |," '{OFS="\t"}{$1=$1;print $0}' | \
		sed '1c rent_date\trent_time\trent_station\treturn_date\treturn_time\treturn_station\trent\tinfodate' |\
		perl -C -pe 's/[^\p{ASCII}\p{Han}]//g'
#	printf "$YearMonth done\n"
else
	unzip -p $1 | \
		awk -F" |," '{OFS="\t"}{$1=$1;print $0}' | \
		sed '1c rent_date\trent_time\trent_station\treturn_date\treturn_time\treturn_station\trent\tinfodate' |\
		iconv -c -f utf-8 -t utf-8
#	printf "$YearMonth done\n"
fi

#unzip -p $1 | \
#	awk -F" |," '{OFS="\t"}{$1=$1;print $0}' | \
#	sed '1c rent_date\trent_time\trent_station\treturn_date\treturn_time\treturn_station\trent\tinfodate' 
