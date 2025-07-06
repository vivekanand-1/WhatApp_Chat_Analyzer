import pandas as pd
import re

def preprocess(chat_txt):
    chat_txt = chat_txt.replace('\u202f', ' ')
    pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [AP]M - '

    dates = re.findall(pattern, chat_txt)
    messages = re.split(pattern, chat_txt)[1:]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    cleaned_messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            cleaned_messages.append(entry[2])
        else:
            users.append("group_notification")
            cleaned_messages.append(entry[0])
    df['user'] = users
    df['message'] = cleaned_messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period']=period



    return df

