import os
import subprocess


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

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
