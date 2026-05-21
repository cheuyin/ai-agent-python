import os
import shutil
from google.genai import types

schema_delete_file = types.FunctionDeclaration(
    name="delete_file",
    description="Delete a file or directory within the working directory. Directories are deleted recursively.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file or directory to delete, relative to the working directory"
            )
        },
        required=["file_path"]
    )
)


def delete_file(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target]) != working_dir_abs:
            return f'Error: Cannot delete "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target):
            return f'Error: "{file_path}" does not exist'

        if os.path.isdir(target):
            shutil.rmtree(target)
            return f'Successfully deleted directory "{file_path}"'
        else:
            os.remove(target)
            return f'Successfully deleted file "{file_path}"'

    except Exception as e:
        return f"Error: {e}"
