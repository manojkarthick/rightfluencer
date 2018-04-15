t = read.csv2('data-tabbed/twitter_influencers_details.csv', sep = ';')
f = read.csv2('data-tabbed/facebook_influencers_details.csv', sep = ';')
i = read.csv2('data-tabbed/instagram_influencers_details.csv', sep = ';')
y = read.csv2('data-tabbed/youtube_influencers_details.csv', sep = ';')
k = read.csv2('data-tabbed/klout_influencers_details.csv', sep = ';')



df <- merge(t,f, by = c('tw_handle'), all.x = T) #merge instock with sales
df <- merge(df, i, by = c('tw_handle'), all.x = T) #merge instock with sales
df <- merge(df, y, by = c('tw_handle'), all.x = T) #merge instock with sales
df <- merge(df, k, by = c('tw_handle'), all.x = T) #merge instock with sales



write.table(df, file = "test.csv", row.names = FALSE, dec = ".", sep = ";", quote = T)

j <- toJSON(df)
write(j, 'test.json')



