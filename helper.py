from urlextract import URLExtract 
extractor = URLExtract()

from collections import Counter

from wordcloud import WordCloud 
import emoji
import pandas as pd

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # num_images = df[df['message'] == 'GIF omitted\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words), len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percent'})
    return x, df 

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500,height = 500,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time 
    
    return timeline 

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend(c for c in message if c in emoji.UNICODE_EMOJI['en'])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df