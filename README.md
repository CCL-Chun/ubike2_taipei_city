# YouBike2.0 Taipei City
## Side project for YouBike2.0 OpenData visualization and analysis

Please visit following [Tableau Dashboard](https://public.tableau.com/views/Youbike2_0tracing/summary?:language=zh-TW&:display_count=n&:origin=viz_share_link)

<div class='tableauPlaceholder' id='viz1696149837812' style='position: relative'><noscript><a href='#'><img alt='summary ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Yo&#47;Youbike2_0tracing&#47;summary&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Youbike2_0tracing&#47;summary' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Yo&#47;Youbike2_0tracing&#47;summary&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='zh-TW' /></object></div>                
<script type='text/javascript'>                    var divElement = document.getElementById('viz1696149837812');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1366px';vizElement.style.height='795px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1366px';vizElement.style.height='795px';} else { vizElement.style.width='100%';vizElement.style.height='2077px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>

# Features
## This repository contains scripts to prepare data tables for visualization and further analysis
### [region_coordinates.sh](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/region_coordinates.sh)
Extract station name, district, longitude and latitude from API response.
[Taipei YouBike2.0 API](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json)
*how to catch can see the code below (catch_taipeicity_ubike2_per_min.py)
### [station_name_check.R](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/station_name_check.R)
This R script handles wired stations name and unifies them for further table join
### [download.sh](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/download.sh)
Download all exist zip files from OpenData (all urls were extracted from csv)
### [read_monthly_data_analysis.R](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/read_monthly_data_analysis.R)
Read all zip files using [data_plastic.sh](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/data_plastic.sh) and process all info corrections, table join and processed tables for visualisation
### [data_plastic.sh](https://github.com/CCL-Chun/ubike2_taipei_city/blob/main/scripts/data_plastic.sh)
Dealing with zip files(csv inside) downloading from youbike2.0 and output tab seperation table
removing characters that didn't support by UTF-8 or other encodes (some stations' name, details in station_name_check.R)
### catch_taipeicity_ubike2_per_min.py

### new_catch_weather_data.py
