import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain,LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
from langchain.callbacks import StreamlitCallbackHandler


## set up the streamlit app
st.set_page_config(page_title="Text To Math Problems Solver Data Search Assistant", page_icon=":robot:")
st.title("Text To Math Problems Solver Data Search Assistant")

# Initialize the Groq model
groq_api_key=st.sidebar.text_input("Enter your Groq API Key", type="password")
if not groq_api_key:
    st.warning("Please enter your Groq API Key to continue.")
else:
    st.success("Groq model initialized successfully!")

# initialize the language model
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)


## initializing the tools
wikipedia = WikipediaAPIWrapper()
wikipedia_tool = Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="Searches Wikipedia for information.",
        return_direct=True
    )

## initializing the Math Tool
math_chain=LLMMathChain.from_llm(
    llm=llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for solving math problems.",
    return_direct=True
    )
prompt="""You are a math problem solver. and mathematical question. logically arrive at the solution and display it point wise for the question below Please solve the following problem:
Question: {question}
Answer:
"""
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)


## combine all the tools into chain
LLMChain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

## Adding reasoning tool
reasoning_tool = Tool(
    name="Reasoning",
    func=LLMChain.run,
    description="Useful for reasoning about math problems.",
    return_direct=True
)

## initializing the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    verbose=True,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I need help with a math problem."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# Lets start the interaction
question = st.text_area("Enter your question ","What is the sum of 2 and 3?",)

if st.button("find my answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb= StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter a question to get an answer.")
