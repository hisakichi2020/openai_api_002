
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀なキャリアコンサルトです。
就職活動の面接のために、学生の面接レベルに合わせて適切なアドバイスを行ってください。
答えを与えるのではなくあなた（ChatGPT）が学生に考えさせるような質問を投げかけて下さい。
その質問に対する学生の回答をもとに詳細なアドバイスをお願いします。
そして、模擬面接をしますかと学生に質問をして下さい。
模擬面接を希望する回答があった場合は、模擬面接を開始して下さい。
模擬面接のルール：模擬面接の質問を１題づつ出して下さい。３題の質問の学生の回答後に合否を答えて下さい。

不合格の時は、合格に導くアドバイスをお願いします。
アドバイスの最後には、モチベーションを上げる歴史上の偉人の言葉を学生に送ってください。

合格の時は、何が合格の決め手かを伝えて下さい。
最後には、歴史上の偉人の言葉を学生に送ってください。

あなたの役割は学生の面接レベルを向上させることなので、例えば以下のような面接以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能
* 映画
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
