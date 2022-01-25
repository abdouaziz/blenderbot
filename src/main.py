import streamlit as st
from streamlit_chat import message as st_message
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


@st.experimental_singleton
def get_models():
    # Load the model and the tokenizer
    tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot_small-90M")

    model = AutoModelForSeq2SeqLM.from_pretrained(
        "facebook/blenderbot_small-90M")

    return tokenizer, model


if "history" not in st.session_state:
    st.session_state.history = []

st.title("Blenderbot")


def generate_answer():
    tokenizer, model = get_models()
    user_message = st.session_state.input_text
    inputs = tokenizer(st.session_state.input_text, return_tensors="pt")
    result = model.generate(**inputs)
    message_bot = tokenizer.decode(
        result[0], skip_special_tokens=True
    )   # decode the result to a string

    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": message_bot, "is_user": False})


st.text_input("Tap to chat with the bot",
              key="input_text", on_change=generate_answer)

for chat in st.session_state.history:
    st_message(**chat)  # unpacking
