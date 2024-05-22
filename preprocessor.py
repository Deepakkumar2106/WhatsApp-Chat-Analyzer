import re
import pandas as pd 
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{2}\s'

    messages = re.split(pattern,data)[1:]

    dates = re.findall(pattern,data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_data type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M:%S ')

    df.rename(columns={'message_date':'date'},inplace=True)

    #separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:#user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'],inplace=True)


    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date 
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df 