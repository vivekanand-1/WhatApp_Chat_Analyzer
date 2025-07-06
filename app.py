#chat_txt is chnge to data
#messages to cleaned_messages
#betacolumns ke jagah if of show analysis me columns ka use hua hai
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("📊 Whatsapp Chat Analyzer")
# by streamlit documentation
uploaded_file = st.sidebar.file_uploader("📁 Choose a chat file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    ## till here file data is in the form of stream so we have to convert it into string
    chat_txt = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(chat_txt)

    # till here we classified our chat into message year date time etc

    #now fetching unique users taaki uske basis pe nikal paaye hum analysis of every user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("👤 Show Analysis WRT",user_list)
    #is button se show hoga analysis

    if st.sidebar.button("🚀 Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        # stats-dikhane ke liye code
        st.title("📌 Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("💬 Total Msges")
            st.subheader(f"**{num_messages}**")
        with col2:
            st.header("✍️ Total Words")
            st.subheader(f"**{words}**")
        with col3:
            st.header("📸 Media Shared")
            st.subheader(f"**{num_media_messages}**")
        with col4:
            st.header("🔗 Links Shared")
            st.subheader(f"**{num_links}**")

        #monthly timeline

        st.title("🗓️ Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()

        ax.plot(timeline['time'], timeline['message'], marker='o', color='green')
        ax.set_title("Monthly Messages")
        ax.set_xlabel("Month-Year", color='purple')
        ax.set_ylabel("Number of Messages", color='purple')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True)
        st.pyplot(fig)

        # Daily Timeline
        st.title("📆 Daily Timeline")
        timeline_data = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline_data['only_date'], timeline_data['message'], marker='o', linestyle='-', color='black')
        ax.set_title("Daily Messages")
        ax.set_xlabel("Date", color='purple')
        ax.set_ylabel("Number of Messages", color='purple')
        plt.xticks(rotation='vertical')
        plt.grid(True)
        st.pyplot(fig)

        #activity map
        st.title('🗺️ Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("📅 Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values, color='skyblue')
            ax.set_title("Most Active Days")
            plt.xticks(rotation='vertical')
            plt.grid(axis='y')
            st.pyplot(fig)

        with col2:
            st.header("📆 Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color = 'orange')
            ax.set_title("Most Active Months")
            plt.xticks(rotation='vertical')
            plt.grid(axis='y')
            st.pyplot(fig)


        # Weekly Activity Heatmap
        st.markdown("🧭 **Weekly Activity Map**")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(user_heatmap, ax=ax, cmap="YlGnBu", linewidths=0.5, linecolor='white', annot=True, fmt='.0f',
                    cbar=True)

        ax.set_xlabel("Time Period", fontsize=12, color='darkblue')
        ax.set_ylabel("Weekday", fontsize=12, color='darkblue')
        ax.set_title("Activity Heatmap", fontsize=14, fontweight='bold', color='black')

        st.pyplot(fig)

        #finding the busiest user in the groip(for group level)
        if selected_user == 'Overall':
            st.title('👥 Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig,ax= plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                ax.set_title("Top 5 Active Users")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2 :
                st.dataframe(new_df)

        #making wordcloud
        st.title("☁️ Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1], color='teal')
        ax.set_title("Most Frequently Used Words")
        plt.xticks(rotation = "vertical")
        st.title("🔠 Most Common Words")
        st.pyplot(fig)

        #  Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("😊 Emoji Analysis")

        if not emoji_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                st.title("🔥 Top 5 Emojis")

                # Set emoji font (Windows path to Segoe UI Emoji)
                import matplotlib.font_manager as fm

                emoji_font_path = "C:/Windows/Fonts/seguiemj.ttf"
                emoji_font = fm.FontProperties(fname=emoji_font_path)

                fig, ax = plt.subplots()
                wedges, texts, autotexts = ax.pie(
                    emoji_df[1].head(),
                    labels=emoji_df[0].head(),
                    autopct="%0.2f"
                )

                # Apply emoji font to pie chart labels
                for text in texts + autotexts:
                    text.set_fontproperties(emoji_font)

                st.pyplot(fig)
        else:
            st.write("No emojis found in the selected chat.")
