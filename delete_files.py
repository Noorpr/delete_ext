import os
from pathlib import Path
import sys



def get_extensions(folder_path: str) -> set:
    extensions= set()
    folder_path = Path(folder_path)
    for file in folder_path.rglob("*"):
        if file.is_file():
            ext = file.suffix.lower()
            if ext:
                extensions.add(ext)
    return sorted(extensions)

def prompt_extensions_to_delete(extensions: set) -> set:
    print("Available file extensions:")
    for ext in extensions:
        print(ext)

    choice = input("Enter the file extensions you want to delete (comma-separated): ")
    selected_extensions = set(choice.split(","))
    for ext in selected_extensions:
        if ext.find(" ") != -1:
            raise ValueError("Invalid input. Please enter valid file extensions.")
    selected_extensions = {ext.strip().lower() for ext in selected_extensions if ext.strip()}
    return selected_extensions


def delete_files(folder_path: str, extensions: set) -> None:
    folder_path = Path(folder_path)

    print(f"Deleting files with extensions: {extensions}")
    count = 0
    for ext in extensions:
        count += len(list(folder_path.rglob(f"*{ext}")))

    print(f"Total files to delete: {count}")

    for ext in extensions:
        for file in folder_path.rglob(f"*{ext}"):
            if file.is_file():
                try:
                    # file.unlink()
                    print(f"Deleted: {file.name}")
                except Exception as e:
                    print(f"Error Deleting {file} : {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    if not os.path.isdir(folder_path):
        print("Invalid input. Please enter a valid folder path.")
        sys.exit(0)
    
    extensions = get_extensions(folder_path)
    if not extensions:
        print("No files found in the specified folder.")
    else:
        selected_extensions = prompt_extensions_to_delete(extensions)
        if len(selected_extensions) == 0:
            print("No extensions selected. Exiting.")
            sys.exit(0)
        else:
            print("Are you sure you want to delete these files? (y/n)")
            
            choice = input()
            if choice.lower() != 'y':
                print("Operation cancelled.")
                sys.exit(0)

            delete_files(folder_path, selected_extensions)
            print("Files deleted successfully.")