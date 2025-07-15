import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler

# -----------------------------
# Set up Streamlit UI
# -----------------------------
st.set_page_config(page_title="Text To Math Problems Solver", page_icon="🧠")
st.title("📊 Text To Math Problems Solver & Wikipedia Assistant")

# -----------------------------
# Get Groq API Key from sidebar
# -----------------------------
groq_api_key = st.sidebar.text_input("🔐 Enter your Groq API Key", type="password")

llm = None
if not groq_api_key:
    st.warning("Please enter your Groq API Key to start.")
else:
    try:
        llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
        st.success("✅ Groq model initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing Groq model: {e}")
        llm = None

# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! I can help solve math problems and fetch info from Wikipedia."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -----------------------------
# Initialize Tools & Agent
# -----------------------------
if llm:
    # Math solving chain
    math_chain = LLMMathChain.from_llm(llm=llm)

    # Wikipedia tool
    wikipedia = WikipediaAPIWrapper()
    wikipedia_tool = Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Use this tool to search Wikipedia for information.",
        return_direct=True
    )

    # Math calculator tool
    calculator = Tool(
        name="Calculator",
        func=math_chain.run,
        description="Use this tool to solve math problems.",
        return_direct=True
    )

    # Reasoning prompt template
    reasoning_prompt = PromptTemplate(
        input_variables=["question"],
        template="""
You are a logical math assistant. Solve the math question below with step-by-step explanation:

Question: {question}
Answer:
"""
    )

    reasoning_chain = LLMChain(llm=llm, prompt=reasoning_prompt)
    reasoning_tool = Tool(
        name="Reasoning",
        func=reasoning_chain.run,
        description="Use this tool for step-by-step reasoning of math problems.",
        return_direct=True
    )

    # Initialize agent with all tools
    assistant_agent = initialize_agent(
        tools=[wikipedia_tool, calculator, reasoning_tool],
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,
        verbose=True,
        handle_parsing_errors=True
    )

    # -----------------------------
    # Main Chat Interface
    # -----------------------------
    question = st.text_area("💬 Enter your question", "What is the sum of 15 and 7?")

    if st.button("🔍 Find Answer"):
        if question.strip() != "":
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            with st.spinner("Thinking..."):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                try:
                    response = assistant_agent.run(question, callbacks=[st_cb])
                except Exception as e:
                    response = f"⚠️ Error: {str(e)}"

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)
        else:
            st.warning("Please enter a question to get an answer.")
