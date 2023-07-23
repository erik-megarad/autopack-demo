import logging
import os

from autopack import Pack
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WriteFileArgs(BaseModel):
    filename: str = Field(
        ...,
        description="Specifies the name of the file to which the content will be written.",
    )
    text_content: str = Field(
        ...,
        description="The content that will be written to the specified file.",
    )


class WriteFile(Pack):
    name = "write_file"
    description = (
        "Allows you to write specified text content to a file, creating a new file or overwriting an existing one as "
        "necessary."
    )
    args_schema = WriteFileArgs
    categories = ["Files"]
    reversible = False

    def _run(self, filename: str, text_content: str):
        try:
            with open(filename, "w+") as f:
                f.write(text_content)
            logger.info(f"Successfully wrote to {filename}")
            return f"Successfully wrote {len(text_content.encode('utf-8'))} bytes to {filename}"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, filename: str, text_content: str):
        return self._run(filename, text_content)


class ReadFileArgs(BaseModel):
    filename: str = Field(
        ...,
        description="The name of the file to be read.",
    )


class ReadFile(Pack):
    name = "read_file"
    description = "Reads and returns the content of a specified file from the disk."
    args_schema = ReadFileArgs
    categories = ["Files"]

    def _run(self, filename: str) -> str:
        """Read a file from disk. If/when we do sandboxing this provides a convenient way to intervene"""
        try:
            # Just in case they give us a path
            filename = os.path.basename(filename)
            file_path = os.path.join(self.body.config.workspace_path, filename)
            if not os.path.exists(file_path):
                return "Error: No such file"

            with open(file_path, "r") as f:
                content = f.read()
                return content

        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, filename: str):
        return self._run(filename)
