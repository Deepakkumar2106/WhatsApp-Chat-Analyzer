import streamlit as st 
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis",user_list)

    if st.sidebar.button("Show Analysis:"):

        num_messages, words, links = helper.fetch_stats(selected_user,df)

        st.title('Top Statistics')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)

        # with col3:
        #     st.header("Media Messages")
        #     st.title(num_images)

        with col3:
            st.header("Links Shared")
            st.title(links)

        #finding the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #wordcloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Weekly Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Days')
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header('Most Busy Months')
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        #Emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
