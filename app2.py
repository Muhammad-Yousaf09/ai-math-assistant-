import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
import re
import math
import operator
import ast

## Set up the Streamlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

## Custom Math Calculator Class
class CustomMathCalculator:
    """A custom math calculator that safely evaluates mathematical expressions"""
    
    # Safe operators and functions
    safe_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    safe_functions = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'exp': math.exp,
        'pi': math.pi,
        'e': math.e,
    }
    
    def _safe_eval(self, node):
        """Safely evaluate an AST node"""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            operator_func = self.safe_operators.get(type(node.op))
            if operator_func:
                return operator_func(left, right)
            else:
                raise ValueError(f"Unsupported operator: {type(node.op)}")
        elif isinstance(node, ast.UnaryOp):
            operand = self._safe_eval(node.operand)
            operator_func = self.safe_operators.get(type(node.op))
            if operator_func:
                return operator_func(operand)
            else:
                raise ValueError(f"Unsupported unary operator: {type(node.op)}")
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name in self.safe_functions:
                args = [self._safe_eval(arg) for arg in node.args]
                return self.safe_functions[func_name](*args)
            else:
                raise ValueError(f"Unsupported function: {func_name}")
        elif isinstance(node, ast.Name):
            if node.id in self.safe_functions:
                return self.safe_functions[node.id]
            else:
                raise ValueError(f"Unsupported variable: {node.id}")
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")
    
    def evaluate(self, expression):
        """Safely evaluate a mathematical expression"""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Handle simple arithmetic expressions
            if re.match(r'^[\d\s\+\-\*\/\(\)\.\^]+$', expression):
                # Replace ^ with ** for exponentiation
                expression = expression.replace('^', '**')
                
                # Parse and evaluate
                tree = ast.parse(expression, mode='eval')
                result = self._safe_eval(tree.body)
                return f"Result: {result}"
            else:
                return "Error: Expression contains unsupported characters or operations"
                
        except Exception as e:
            return f"Error: Could not evaluate expression - {str(e)}"

# Create custom calculator instance
calculator_instance = CustomMathCalculator()

## Initialize the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned"
)

## Custom Math Tool
def math_calculator(expression):
    """Custom math calculator function"""
    return calculator_instance.evaluate(expression)

calculator = Tool(
    name="Calculator",
    func=math_calculator,
    description="A tool for answering math related questions. Only input mathematical expressions like '2+2', '10*5', '(4+6)/2', etc."
)

## Enhanced Math Reasoning Prompt
math_prompt = """
You are a mathematical problem solver. Your task is to solve the given mathematical question step by step.

Instructions:
1. Read the problem carefully and identify what needs to be calculated
2. Break down complex problems into smaller steps
3. Use the Calculator tool for arithmetic operations (format: just the mathematical expression like "2+3" or "10*4")
4. Show your work clearly
5. Provide the final answer

For calculation steps, use simple expressions like:
- Addition: "5+3"
- Subtraction: "10-4" 
- Multiplication: "6*7"
- Division: "20/4"
- Parentheses: "(5+3)*2"

Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=math_prompt
)

## Combine all the tools into chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions with step-by-step mathematical solutions."
)

## Initialize the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

## Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions"}
    ]

## Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

## Let's start the interaction
question = st.text_area(
    "Enter your question:", 
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?"
)

if st.button("Find My Answer"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            
            try:
                response = assistant_agent.run(question, callbacks=[st_cb])
                st.session_state.messages.append({'role': 'assistant', "content": response})
                st.write('### Response:')
                st.success(response)
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({'role': 'assistant', "content": error_msg})
    else:
        st.warning("Please enter a question")
