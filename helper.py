from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = sum(len(msg.split()) for msg in df['message'])
    media_msgs = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = sum(len(extract.find_urls(msg)) for msg in df['message'])

    return num_messages, words, media_msgs, links

def most_busy_users(df):
    top = df['user'].value_counts().head()
    percent_df = round(df['user'].value_counts(normalize=True) * 100, 2).reset_index()
    percent_df.columns = ['name', 'percent']
    return top, percent_df

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>|This message was deleted', case=False, na=False)]

    temp['message'] = temp['message'].apply(lambda msg: " ".join([word for word in msg.lower().split() if word not in stop_words]))
    wc = WordCloud(width=500, height=500, background_color='black')
    return wc.generate(temp['message'].str.cat(sep=" "))

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>|This message was deleted', case=False, na=False)]

    words = []
    for msg in temp['message']:
        words.extend([word for word in msg.lower().split() if word not in stop_words])
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for msg in df['message']:
        emojis.extend([ch for ch in msg if emoji.is_emoji(ch)])
    return pd.DataFrame(Counter(emojis).most_common())

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.groupby('only_date').count()['message'].reset_index()

def hourly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.groupby('hour').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap

def longest_messages(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['msg_length'] = df['message'].apply(len)
    return df[['user', 'message', 'msg_length']].sort_values(by='msg_length', ascending=False).head(10)

def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    def analyze_sentiment(msg):
        return TextBlob(msg).sentiment.polarity

    df['sentiment'] = df['message'].apply(analyze_sentiment)
    return df[['user', 'message', 'sentiment']].sort_values(by='sentiment', ascending=False)
