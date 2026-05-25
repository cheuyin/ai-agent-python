import os
import subprocess
from google.genai import types
from config import MAX_CHARS

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file and see its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments for the Python script",
                items=types.Schema(type=types.Type.STRING)
            )
        },
        required=["file_path"]
    )
)


def run_python_file(working_directory, file_path: str, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        process: subprocess.CompletedProcess = subprocess.run(
            command, text=True, timeout=30, capture_output=True, cwd=working_dir_abs)

        output = []
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")

        if not process.stdout and not process.stderr:
            output.append("No output produced")

        if process.stdout:
            output.append(f"STDOUT:\n{process.stdout}")

        if process.stderr:
            output.append(f"STDERR:\n{process.stderr}")

        result = "\n".join(output)
        if len(result) > MAX_CHARS:
            result = result[:MAX_CHARS] + f"\n[...Output truncated at {MAX_CHARS} characters]"
        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
