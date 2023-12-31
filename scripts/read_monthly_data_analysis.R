#!/bin/Rscript
#CCL-Chun update at 2023/09/27

#Set working dir
setwd("working/dir")
#Library used in this script
library(data.table)
library(dplyr)
library(multidplyr)
library(chron)

#Read csv from zip-files and pre-process for unifying format
#Call the data_plastic.sh and save the STDOUT to all_df 
files <- list.files(full.names=T,pattern="*.zip")
#Get output from data_plastic.sh and merge together
all_df <- rbindlist(lapply(
  files,function(f) fread(cmd=paste("bash data_plastic.sh",f))))

#Create time specific columns
all_df$Year <- year(all_df$rent_date)
all_df$Month <- month(all_df$rent_date)
all_df$rent <- times(all_df$rent)
long_time <- all_df[is.na(all_df$rent),] #long renting time 
all_df <- all_df[is.na(all_df$rent)==F,] #filter out renting time >24hr
all_df$time_spent_sec <- as.numeric(all_df$rent)*86400 #seconds
all_df$time_spent_mins <- round(all_df$time_spent_sec / 60) #minutes

#Correcting stations' name
#read the correction file from station_name_check.R
name_complete <- read.table("completed_station_name.txt",header = T) 
for (i in c(1:length(name_complete$station))) {
  all_df$rent_station[all_df$rent_station==name_complete$station[i]] <- name_complete$all_name[i]
}
#Save raw dataframe
#fwrite(all_df,"all_records.txt",quote = F,sep = "\t",row.names = F)

#Reload dataframe 
#all_df <- fread("all_records.txt")
#Read station details table
details <- read.table("site_details_Taipei.txt",header = T)

##basic stats
pop_time <- all_df %>% 
  group_by(Year,Month,rent_time) %>% 
  summarise(n=n(),avg_time_spent=mean(rent),
            avg_spent_sec=mean(time_spent_sec),SD=sd(rent),
            quantiles = list(quantile(time_spent_sec))) %>% 
  unnest_wider(quantiles, names_sep = "_") %>%
  rename_with(~ c("Q0", "Q1", "Q2", "Q3", "Q4"), starts_with("quantiles"))
write.table(pop_time,"pop_time.txt",sep = "\t",quote = F,row.names = F)

#Try multidplyr to parallel the large data
cluster <- new_cluster(16) #the number depends on the device
cluster_library(cluster, "dplyr")
cluster_library(cluster, "chron")

pop_path_by_month <- all_df %>% 
  group_by(Year,Month,rent_station,return_station) %>% 
  partition(cluster) %>% #parallel
  summarise(n=n(),avg_time_spent=times(mean(rent)),
           avg_spent_sce=mean(time_spent_sec)) %>%
  mutate(path=paste(rent_station,return_station,sep = "__")) %>% 
  collect() #gather data from parallel
write.table(pop_path_by_month,"pop_path_by_month.txt",sep = "\t",quote = F,row.names = F)

#Try dtplyr and magrittr to handle large data and pipe
library(dtplyr)
library(magrittr)

all_df_dt <- lazy_dt(all_df)
details_dt <- lazy_dt(details)

all_df_dt %>% left_join(details_dt,by=c('rent_station'='station')) %>% 
  left_join(details_dt,by=c('return_station'='station')) %>%
  filter(is.na(city.x)!=T & is.na(city.y)!=T) %T>% #tee pipe
  {joined_df <<- .; .} %T>% #tee pipe
  {dist_rent_spent <<- group_by(.,Year,Month,area.x,time_spent_mins) %>% 
                    summarise(n=n()) %>% as.data.frame(); . } %>% 
  group_by(Year,Month,area.y,time_spent_mins) %>% summarise(n=n()) %>%
  as.data.frame() -> dist_return_spent

#Prepare table for the spent time distribution
dist_rent_spent %<>% 
  mutate(time_spent_mins = ifelse(time_spent_mins > 70, 70, time_spent_mins)) %>% 
  group_by(Year,Month,area.x,time_spent_mins) %>% summarise(n=sum(n))
dist_return_spent %<>% 
  mutate(time_spent_mins = ifelse(time_spent_mins > 70, 70, time_spent_mins)) %>% 
  group_by(Year,Month,area.x,time_spent_mins) %>% summarise(n=sum(n))

write.table(dist_rent_spent,"dist_rent_spent.txt",quote = F,row.names = F)
write.table(dist_return_spent,"dist_return_spent.txt",quote = F,row.names = F)


