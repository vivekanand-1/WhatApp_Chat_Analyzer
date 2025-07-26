import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="WhatsApp Chat Analyzer")

st.sidebar.title("📊 Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("📁 Choose a chat file (.txt only)")

if uploaded_file is not None:
    chat_txt = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(chat_txt)

    user_list = df['user'].unique().tolist()
    user_list = sorted([user for user in user_list if user != 'group_notification'])
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Show Analysis WRT", user_list)

    if st.sidebar.button("🚀 Show Analysis"):
        st.title("📌 Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 Total Messages", num_messages)
        col2.metric("✍️ Total Words", words)
        col3.metric("📸 Media Shared", num_media_messages)
        col4.metric("🔗 Links Shared", num_links)

        st.title("🗓️ Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], marker='o', color='green')
        ax.set_title("Monthly Messages")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.title("📆 Daily Timeline")
        daily_data = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_data['only_date'], daily_data['message'], color='black')
        ax.set_title("Daily Messages")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.title('⏰ Hourly Activity')
        hourly_activity = helper.hourly_activity(selected_user, df)
        fig, ax = plt.subplots()
        sns.lineplot(data=hourly_activity, x='hour', y='message', ax=ax, color='orange', marker='o')
        ax.set_xticks(range(24))
        st.pyplot(fig)

        st.title("🗺️ Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='skyblue')
            st.pyplot(fig)

        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)

        st.markdown("### 🧭 Weekly Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap, cmap='YlGnBu', annot=True, fmt='g')
        st.pyplot(fig)

        if selected_user == "Overall":
            st.title("👥 Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("☁️ Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        st.title("🔠 Most Common Words")
        common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_df[0], common_df[1], color='teal')
        plt.xticks(rotation=0)
        st.pyplot(fig)

        st.title("📏 Longest Messages")
        long_df = helper.longest_messages(selected_user, df)
        st.dataframe(long_df)

        st.title("😊 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        if not emoji_df.empty:
            col1, col2 = st.columns(2)
            col1.dataframe(emoji_df.head(10))
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%")
                st.pyplot(fig)
        else:
            st.write("No emojis found.")

        st.title("📉 Sentiment Analysis (Experimental)")
        sentiment_df = helper.sentiment_analysis(selected_user, df)
        st.dataframe(sentiment_df.head(10))
