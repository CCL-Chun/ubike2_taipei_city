 awk '{OFS="\t"}{print $2,$5,$8,$9}' api_catch/R_code/data_2023-08-30\ 12\:18\:40.txt |sed 's/YouBike2.0_//g' > site_details.txt

 awk '{OFS="\t"}{print $2,$5,$7,$8}' api_catch/py_code2.0/data_2023-08-30_12-10-40.txt |sed 's/YouBike2.0_//g' > site_details_newTaipei.txt
