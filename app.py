import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import chatToDataframe
import analysisAPI as helper
import webbrowser
import base64


col1, col2 = st.columns(2)

with col1:
    file_ = open("./animate.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" style="margin-bottom:40px" width=300 alt="animate gif">',
        unsafe_allow_html=True,
    )
with col2:
    st.title("😎 Hi Everyone My name is Aadil.")
    st.markdown(f"<h4>This is the whatApp chat Analyser Web App to get insight from your Groups as well as your individual chats.</h4>",
                unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🫧 My Resume   "):
        webbrowser.open('https://aadilmughal786.github.io/My_web_resume')
with col2:
    if st.button("🫧 My Githib"):
        webbrowser.open('https://github.com/aadilmughal786')
with col3:
    if st.button("🫧 My Linkedin"):
        webbrowser.open(
            'https://www.linkedin.com/in/aadil-mugal-146bb818a')
with col4:
    if st.button("🫧 Tutorial link"):
        webbrowser.open('https://www.youtube.com/watch?v=Q0QwvZKG_6Q')

st.markdown(f"<p style='text-align: center;margin:10px 0px 10px;'>{'🌱'*35}</p>",
            unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;color:green;'>🕐Dates must be in 24 hours format</h1>",
            unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='text-align: center;'>✨</h1>",
                    unsafe_allow_html=True)
st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a chat file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = chatToDataframe.preprocess(data)

    st.title("Full Dataframe")
    st.dataframe(df, use_container_width=True)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "All users")

    # select box
    selected_user = st.sidebar.selectbox("Select user", user_list)

    # display Analysis
    if st.sidebar.button("Display Analysis"):

        st.title("Top Statistics")
        file__ = open("./Data-Inspect.gif", "rb")
        contents = file__.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file__.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" style="margin-bottom:40px;width:100%;"  alt="animate gif">',
            unsafe_allow_html=True,
        )

        # Stats Area
        num_messages, words, num_media_messages, num_links, df = helper.fetch_stats(
            selected_user, df)

        # display user specific data
        if selected_user != 'All users':
            st.title(f"{selected_user}'s chat")
            st.dataframe(df[["message", "date"]], use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Links Shared")
            st.title(num_links)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Total Words")
            st.title(words)

        # finding the busiest users in the group(Group level)
        if selected_user == 'All users':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df, use_container_width=True)

        # WordCloud and most common words
        st.title("Wordcloud")
        df_wc, most_common_df = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='green')
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_analysis(selected_user, df)
        st.title("Emoji Analysis")

        try:
            st.title("Top 5 emojis pi-chart")
            emojiTop5 = ["Emoji-0", "Emoji-1",
                         "Emoji-2", "Emoji-3", "Emoji-4"]
            fig, ax = plt.subplots()
            ax.pie(emoji_df["Frequincy"].head(),
                   labels=emojiTop5, autopct="%0.2f")
            st.pyplot(fig)

            st.title("Emoji Frequincy table")
            st.dataframe(emoji_df, use_container_width=True)
        except:
            st.title("There is no emojis in this chat to analysis")

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'],
                daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Weekly Activity Heat Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.markdown("<h2 style='text-align: center;'>Thanks for using this App.</h2>",
                    unsafe_allow_html=True)

        st.markdown("<h4 style='text-align: center;margin-top:80px;'>Made by Aadil Mugal Made with <span style='color:red;'>🎔</span></h4>",
                    unsafe_allow_html=True)
