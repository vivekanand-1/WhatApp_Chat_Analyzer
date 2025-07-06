#drawback media ommited is counted twice
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # 1. num of messages
    num_messages = df.shape[0]
    # 2. num of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    #fetch media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    #fetch number of links shared
    links= []
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):

    x = df['user'].value_counts().head()
    #df= round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        #columns={'index': 'name', 'user': 'percent'}) iske jagah
    df = (df['user'].value_counts(normalize=True) * 100).round(2).reset_index()
    df.columns = ['name', 'percent']

    return x,df



def create_wordcloud(selected_user, df):
    # Load stop words
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out system messages
    temp = df[df['user'] != 'group_notification'].copy()
    temp = temp[~temp['message'].str.lower().str.contains(r'<media omitted>|this message was deleted', na=False)]

    # Remove stop words
    def remove_stop_words(message):
        words = [word for word in message.lower().split() if word not in stop_words]
        return " ".join(words)

    temp['message'] = temp['message'].apply(remove_stop_words)

    # Generate word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    # removing group notification
    temp = df[df['user'] != 'group_notification']
    # remove media ommited and this message was deleted
    temp = temp[~temp['message'].str.lower().str.contains(r'<media omitted>|this message was deleted', na=False)]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    #here the name was daily_timeline it is changed daily_timelin
    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline_df

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):


    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Ensure weekday order (optional: convert to categorical with order)
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day_name'] = pd.Categorical(df['day_name'], categories=ordered_days, ordered=True)

    # Create heatmap pivot table
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap





