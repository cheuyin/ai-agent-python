import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to the specified file within the working directory (overwriting it if the file exists). NOTE: This function will create the directories in its path if they don't already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing to file: {e}"
