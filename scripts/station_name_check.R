setwd("/mnt/sda1/Kevin/ubike")
library(data.table)
library(httr)
library(jsonlite)
library(dplyr)

details <- read.table("site_details.txt",header = T)
colnames(details) <- c("station","area","Latitude","Longitude")
details$city <- "台北市"

new_taipei <- read.table("site_details_newTaipei.txt",header = F)
new_taipei$city <- "新北市"
colnames(new_taipei) <- colnames(details)
details <- rbind(details,new_taipei)
duplicate_name <- details %>% group_by(station) %>% 
  summarise(n=n()) %>% filter(n>1) ##find out replicate name between cities
details$station[details$station %in% duplicate_name$station & details$city=="新北市"] <- 
  paste(details$station[details$station %in% duplicate_name$station & details$city=="新北市"],"新北",sep = "_")
write.table(details,"site_details_Taipei.txt",row.names = F,quote = F)
##高雄站名
api_url <- "https://api.kcg.gov.tw/api/service/Get/b4dd9c40-9027-4125-8666-06bef1756092"
response <- GET(api_url, timeout(60))
data <- content(response, as = "text") %>%
  fromJSON(flatten = TRUE)
site_ks <- data[["data"]][["retVal"]]
site_ks <- site_ks[,c(1,3)]
site_ks$sna <- gsub("YouBike2.0_",x = site_ks$sna,"")
colnames(site_ks) <- c("city","station")

library(fuzzyjoin)
library(stringdist)
library(stringr)
library(purrr)

cluster <- new_cluster(8)
cluster_library(cluster, "dplyr")

tt <- all_df %>% 
  left_join(details,by=c("rent_station" = "station"))
colnames(tt)[c(12:14)] <- c("rent_area","rent_Longitude","rent_Latitude")
tt_un <- tt[is.na(tt$rent_area),c(1:11)]

un_classify <- as.data.frame(unique(tt_un$rent_station))
colnames(un_classify)="station"
un_classify <- un_classify %>% filter(station!="")
un_classify <- un_classify %>% left_join(site_ks)
ks_found <- un_classify %>% filter(city=="高雄市")
un_classify <- un_classify %>%  
  filter(is.na(city)==T) %>% 
  mutate(all_name=
           map_chr(station,
                   ~if_else(
                     any(str_detect(details$station,fixed(.x))),
                     details$station[str_detect(details$station,fixed(.x))][1],
                     NA_character_)))
name_complete <- un_classify %>% filter(is.na(all_name)==F) %>% select(-"city")
un_classify <- un_classify %>% 
  filter(is.na(all_name)==T) %>% 
  mutate(all_name=case_when(
    station == "臺大仰萃樓東南側" ~ "臺大禮賢樓東南側",
    station == "捷運台北小巨蛋站(2號出口)" ~ "捷運小巨蛋站(2號出口)",
    station == "捷運善導寺站(3號出口)(忠孝路" ~ "捷運善導寺站(3號出口)(忠孝東路側)"))
name_complete <- un_classify %>% filter(is.na(all_name)==F) %>% 
  select(-"city") %>% rbind(name_complete)

un_classify <- un_classify %>% 
  filter(is.na(all_name)==T) %>% 
  mutate(all_name=
      map_chr(station,
              ~details$station[str_detect(details$station,regex(gsub("[?]",".",.x)))][1]))
name_complete <- un_classify %>% filter(is.na(all_name)==F) %>% 
  select(-"city") %>% rbind(name_complete)

un_classify <- un_classify %>% 
  filter(is.na(all_name)==T) %>% select(-c("city","all_name")) %>% 
  stringdist_left_join(details,max_dist=1) 
name_complete <- un_classify %>% filter(is.na(station.y)==F) %>% 
  select(c(1,2)) %>% rename(station=station.x,all_name=station.y) %>% 
  rbind(name_complete)
  
write.table(name_complete,"completed_station_name.txt",sep = "\t",
            row.names = F,quote = F)
#####################changed name##############
######## Original  ##################  New  ##################
#####臺大仰萃樓東南側#############臺大禮賢樓東南側############
##捷運台北小巨蛋站(2號出口)######捷運小巨蛋站(2號出口)###########
##捷運善導寺站(3號出口)(忠孝路  ====>  捷運善導寺站(3號出口)(忠孝東路側)#####



