#必要なものをimport
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

#Openai APIキーを環境変数から読み込む
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#課題のタイトルを記載
st.title("提出課題")

#ラジオボタンで動作モードを選択
selected_item = st.radio(
    "動作モードを選択してください。/n２種類の専門家をラジオボタンで選んだ後、依頼を入力してください",
    ["料理の専門家", "運動の専門家"]
)
#選択された動作モードに応じた入力フォームを表示
st.divider()

#ラジオボタンで選択
if selected_item == "料理の専門家":
    system_message = ""
    system_message += "あなたは料理の専門家です。料理についての質問に回答し、それ以外の質問は「専門外で回答できません」と回答してください"
else:
    system_message = ""
    system_message += "あなたは運動の専門家です。運動についての質問に回答し、それ以外の質問は「専門外で回答できません」と回答してください"

input_message = st.text_input(label="依頼を入力してください。")

# LLMの初期化
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

if st.button("実行"):
    if input_message:  # 入力が空でない場合のみ実行
        st.divider()
        
        # メッセージの作成
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=input_message),
        ]
        
        # LLMを呼び出して応答を取得
        try:
            with st.spinner("回答を生成中..."):
                response = llm.invoke(messages)
            
            # 応答を表示
            st.subheader("回答:")
            st.write(response.content)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("依頼を入力してください。")
    