"""Code Interpreter tool spec."""

from llama_index.core.tools.tool_spec.base import BaseToolSpec
import tempfile
import os
import docker

class CodeInterpreterToolSpec(BaseToolSpec):
    """Code Interpreter tool spec."""

    spec_functions = ["code_interpreter"]

    def code_interpreter(self, code: str):
        """
        A function to execute python code, and return the stdout and stderr.


        You should import any libraries that you wish to use. You have access to any libraries the user has installed.


        The code passed to this functuon is executed in isolation. It should be complete at the time it is passed to this function.


        You should interpret the output and errors returned from this function, and attempt to fix any problems.
        If you cannot fix the error, show the code to the user and ask for help


        It is not possible to return graphics or other complicated data from this function. If the user cannot see the output, save it to a file and tell the user.
        """
        with tempfile.NamedTemporaryFile(suffix=".py", delete=True) as temp_file:
            temp_file.write(code.encode())
            temp_file.flush()
            temp_file_path = temp_file.name

            try:
                client = docker.from_env()
                result = client.containers.run(
                    "python:3.10-alpine",
                    command=["python", os.path.basename(temp_file_path).split('/')[-1]],
                    volumes={os.path.dirname(temp_file_path):{"bind":"/usr/src/mycode"}},
                    working_dir="/usr/src/mycode",
                    remove=True
                )
                return result
            except Exception as e:
                return f"Error: {e}"