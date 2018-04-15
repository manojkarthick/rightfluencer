import pandas as pd
from functools import reduce

tw_df = pd.read_csv('twitter_influencers_details.csv', sep=';')
ig_df = pd.read_csv('instagram_influencers_details.csv', sep=';')
yt_df = pd.read_csv('youtube_influencers_details.csv', sep=';')
kl_df = pd.read_csv('klout_influencers_details.csv', sep=';')
fb_df = pd.read_csv('facebook_influencers_details.csv', sep=';')

dfs = [tw_df, ig_df, yt_df, fb_df, kl_df]
df_final = reduce(lambda left,right: pd.merge(left,right,on='tw_handle', how='left'), dfs)

df_final.to_csv('sample.csv', sep=';', index=False)