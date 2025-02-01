import streamlit as st  # type: ignore
from langchain_ollama import ChatOllama
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Streamlit UI
st.title("Voice from the Sietch 🌕")
st.write("Ask me anything about the **Dune universe**—no spoilers!")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# System prompt for spoiler-free, Dune-focused responses
system_prompt = SystemMessage(content="""
You are a Dune historian and expert, providing **detailed, spoiler-free** insights about the Dune universe. 

Guidelines:
- **DO NOT** reveal major plot twists, character fates, or hidden motives.
- **DO** explain themes, factions, planets, and general world-building.
- **DO** help new readers/watchers understand the universe without spoilers.
- **IF** asked for spoilers, respond with:  
  "I aim to keep the mystery alive! Let’s explore the world of Dune without revealing surprises."
  
**Rules:**
- If a question is NOT about Dune, say:  
  "I only discuss the majestic world of Dune! Ask me about Arrakis, spice, or anything related to the Dune universe."
- NEVER provide responses outside the Dune universe.
- NO spoilers—explain without revealing major plot twists.
""")

# Function to generate AI responses
def generate_response(input_text):
    model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")

    chat_history = [
        system_prompt,
        *[HumanMessage(content=msg["user"]) for msg in st.session_state["chat_history"]],
        HumanMessage(content=input_text)
    ]
    response = model.invoke(chat_history)
    return response.content

# User input form
with st.form("llm-form"):
    text = st.text_area("Enter your question about Dune:")
    submit = st.form_submit_button("Submit")

# Process user input
if submit and text:
    with st.spinner("Navigating the desert of knowledge..."):
        response = generate_response(text)

        # Append user input and AI response to chat history
        st.session_state["chat_history"].append({"user": text, "ollama": response})

        # Display latest response
        st.subheader("Echoes from Arrakis say:")
        st.write(response)

# Display chat history
st.write("## Chat History")
for chat in st.session_state["chat_history"]:
    st.write(f"🦹🏻 **User:** {chat['user']}")
    st.write(f"💬 **VOICE:** {chat['ollama']}")
    st.write("---")  # Separator for readability
