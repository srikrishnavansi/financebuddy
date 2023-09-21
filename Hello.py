from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re
import os
import streamlit as st
from langchain.retrievers.web_research import WebResearchRetriever      
from elevenlabs import set_api_key

def setup():
    OPENAI_API_KEY = st.text_input("Enter your OPENAI GPT4 API KEY:", type="password")
    GOOGLE_CSE_ID = st.text_input("Enter your GOOGLE CSE ID:", type="password")
    GOOGLE_API_KEY = st.text_input("Enter your GOOGLE API KEY:", type="password")
    # Set the environment variables
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

    if st.button("Submit"):
        st.success("Successfully Setup keys")
        st.success("Please go to Chat section")

def app():
    # Function for web scraping tool
    def web_scraping_tool(query: str) -> str:
        import urllib.parse
        from googleapiclient.discovery import build

        # Replace with your own API key and CSE ID
        GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
        GOOGLE_CSE_ID = "YOUR_GOOGLE_CSE_ID"

        # URL-encode the query
        encoded_query = urllib.parse.quote(query)

        # Build the Google Custom Search service
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

        try:
            # Make the API request
            result = service.cse().list(q=encoded_query, cx=GOOGLE_CSE_ID, num=1).execute()
            if "items" in result:
                # Extract the first result (you can modify this as needed)
                first_result = result["items"][0]["link"]
                return first_result
            else:
                return "No results found"
        except Exception as e:
            return f"Error: {str(e)}"

    # List of available tools
    tools = [
        Tool(
            name="WebScraping",
            func=web_scraping_tool,
            description="Useful for scraping information from websites and the internet."
        ),
    ]

    # Defining chat prompts
    # (Please note that prompt variables are repeated and will need to be maintained in sync)
    prompt = """
    Hey AI, your name is Sunny, Your Financial Buddy. Please act as if you're my close friend, not a professional, and let's talk about my financial goals and plans. Your tone should be warm, friendly, and reassuring, just like a trusted friend. Feel free to guide me through financial decisions and offer advice as you would to a close buddy.

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be {tool_names}
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    These were previous tasks you completed:
    {history}
    Begin!

    Question: {input}
    {agent_scratchpad}"""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Set up a prompt template
    class CustomPromptTemplate(BaseChatPromptTemplate):
        template: str
        tools: List[Tool]

        def format_messages(self, **kwargs) -> str:
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            kwargs["agent_scratchpad"] = thoughts
            kwargs["history"] = st.session_state.messages
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
            formatted = self.template.format(**kwargs)
            return [HumanMessage(content=formatted)]

    # Creating a custom prompt
    prompt = CustomPromptTemplate(
        template=prompt,
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )

    # Custom output parser
    class CustomOutputParser(AgentOutputParser):

        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )

            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if match:
                action = match.group(1).strip()
                action_input = match.group(2).strip(" ").strip('"')
                return AgentAction(tool=action, tool_input=action_input, log=llm_output)

            if "\nObservation:" in llm_output:
                observation = llm_output.split("\nObservation:", 1)[-1].strip()
                return AgentAction(tool="Observation", tool_input="", log=llm_output)

            return AgentFinish(
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )

    # Creating an output parser
    output_parser = CustomOutputParser()

    # Initializing ChatOpenAI model
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.8)

    # Creating an LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # List of tool names
    tool_names = [tool.name for tool in tools]

    # Creating an LLMSingleActionAgent
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )

    # Creating an AgentExecutor
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    # Streamlit chat interface
    st.markdown("<h1 align=center>💲FinSight - Your Finance Buddy📈</h1>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask a Question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            ai_response = agent_executor.run(prompt)
            message_placeholder.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

def home_page():
    # HTML code for the welcome message
    welcome_message = """
    <div style="text-align: center;">
        <h1>Welcome <br> 💲FinSight - Your Finance Buddy📈</h1>
        <p>To get started, please go to <a href='#' onclick='open_settings()'>Settings</a> and set up your API keys.</p>
    </div>

    <script>
        // JavaScript function to open the Settings page
        function open_settings() {
            window.location.href = '#Settings';
        }
    </script>
    """

    # Display the welcome message using st.markdown
    st.markdown(welcome_message, unsafe_allow_html=True)

def main():
    st.sidebar.title("FinSight")
    selected_page = st.sidebar.radio("Go to:", ["Home", "Settings", "Chat"])
    if selected_page == "Home":
        home_page()
    elif selected_page == "Settings":
        setup()
    elif selected_page == "Chat":
        app()

main()
