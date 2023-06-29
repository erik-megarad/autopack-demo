#!/usr/bin/env python
import json

from autopack.api import pack_search
from autopack.errors import AutoPackError
from autopack.installation import install_pack
from autopack.pack import Pack
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

TOOL_SELECTION_PROMPT = """
I have a list of tools to choose from and a task I need to accomplish. Please tell me all of the tools that are
necessary for me to accomplish my task. Respond only with the tool_ids as a valid JSON array.

---- TASK ----
{user_input}
---- TOOLS ----
{tools_string}
"""


def select_packs(user_input: str, llm: ChatOpenAI) -> list:
    packs = pack_search("")
    pack_summaries = {}
    for pack in packs:
        # For now this only works with packs that have no init args, so filter those out
        if pack.init_args:
            continue

        pack_summaries[pack.pack_id] = {
            "tool_id": pack.pack_id,
            "name": pack.name,
            "description": pack.description,
            "arguments": pack.run_args,
        }

    tools_string = json.dumps(pack_summaries)
    prompt = TOOL_SELECTION_PROMPT.format(
        user_input=user_input, tools_string=tools_string
    )
    message = HumanMessage(content=prompt)

    response = llm(messages=[message])
    return json.loads(response.content)


def install_packs(pack_ids: list[str]) -> list[Pack]:
    packs = []
    for pack_id in pack_ids:
        try:
            packs.append(install_pack(pack_id, force_dependencies=True))
        except AutoPackError as e:
            print(
                f"Pack {pack_id} could not be installed, leaving it out of the toolset. {e}"
            )
            continue

    return packs


def main():
    print("What would you like me to do?")
    print("> ", end="")
    user_input = input()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")

    pack_ids = select_packs(user_input, llm)
    packs = install_packs(pack_ids)

    for pack in packs:
        # TODO: Automatically determine how to pass init args. e.g. map env variables to API key args
        pack.init_tool()

    agent_executor = initialize_agent(
        packs,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_executor.run(user_input)


if __name__ == "__main__":
    main()
