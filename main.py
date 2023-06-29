#!/usr/bin/env python

from autopack.get_pack import try_get_pack
from autopack.pack import Pack
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import WriteFileTool

load_dotenv()

DEMO_PACK_IDS = [
    "erik-megarad/my_tools/os_info",
    "erik-megarad/my_tools/disk_usage",
]


def get_packs(pack_ids: list[str]) -> list[Pack]:
    packs = []
    for pack_id in pack_ids:
        pack = try_get_pack(pack_id)
        if pack:
            packs.append(pack)

    return packs


def main():
    packs = get_packs(DEMO_PACK_IDS)
    [pack.init_tool() for pack in packs]
    # TODO: Fix this once langchain is re-indexed
    packs.append(WriteFileTool())

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
