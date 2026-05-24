import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
            )
        }
    )
)


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath(
            [working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result_str = ""

        for item in sorted(os.listdir(target_dir)):
            if item.startswith("."):
                continue
            item_path = os.path.join(target_dir, item)
            size_str = f"{str(os.path.getsize(item_path))} bytes"
            is_dir = os.path.isdir(item_path)
            new_line = f"- {item}: file_size={size_str}, is_dir={is_dir}"
            result_str += new_line + "\n"

        return result_str

    except Exception as e:
        return f"Error: {e}"
