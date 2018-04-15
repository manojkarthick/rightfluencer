from klout import Klout

api_key = 'qzcujyjgy7b554kw9htud9ny'
k = Klout(api_key, secure=True)

def get_handle(url):
    splits = url.split('/')
    if url:
        if url.endswith('/'):
            handle = splits[-2]
        else:
            handle = splits[-1]
    else:
        handle = None    
    return handle

def get_klout_id(screen_name):
    kloutId = k.identity.klout(screenName=screen_name).get('id')
    return kloutId

def get_klout_score(kloutId):
    score = k.user.score(kloutId=kloutId, timeout=5).get('score')
    return score

df = pd.read_csv('twitter_influencers_details.csv',sep=';')

columns = ['tw_handle', 'tw_screen_name', 'kl_id,', 'kl_score']
outdf = pd.DataFrame(columns=columns)

for index, row in df.iterrows():
    tw_handle = row['tw_handle']
    tw_screen_name = row['tw_screen_name']
    kloutId = get_klout_id(tw_screen_name)
    score = get_klout_score(kloutId)
    
    result_list = [tw_handle, tw_screen_name, kloutId, score]
    outdf.loc[index] = result_list

outdf.to_csv('klout_influencers_details.csv', sep=';', index=False)