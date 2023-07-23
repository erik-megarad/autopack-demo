#!/usr/bin/env python
import logging

from autopack.api import pack_search
from autopack.errors import AutoPackError
from autopack.installation import install_pack
from autopack.pack import Pack
from autopack.selection import select_packs
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

from demo.packs import WriteFile, ReadFile

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def install_all_packs() -> list[Pack]:
    pack_search_response = pack_search("")
    packs = []
    for pack_response in pack_search_response:
        try:
            installed_pack = install_pack(pack_response.pack_id, force_dependencies=True)
            packs.append(installed_pack)
        except AutoPackError as e:
            logger.error(f"Pack {pack_response.pack_id} could not be installed, leaving it out of the toolset. {e}")
            continue

    return packs


def main():
    print("What would you like me to do?")
    print("> ", end="")
    user_input = input()

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k-0613")

    install_all_packs()
    packs = select_packs(user_input, llm=llm)
    packs += [ReadFile, WriteFile]

    wrappers = [pack(llm=llm).init_langchain_tool() for pack in packs]

    if not packs:
        logger.error("No packs are installed, continuing is not viable")
        exit()

    agent_executor = initialize_agent(
        wrappers,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_executor.run(user_input)


if __name__ == "__main__":
    main()
