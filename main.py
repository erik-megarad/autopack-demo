#!/usr/bin/env python
from autopack.get_pack import get_all_installed_packs
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

load_dotenv()


def main():
    packs = get_all_installed_packs()
    [pack.init_tool() for pack in packs]

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")

    agent_executor = initialize_agent(
        packs,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    print("What would you like me to do?")
    print("> ", end="")
    user_input = input()
    agent_executor.run(user_input)


if __name__ == "__main__":
    main()
