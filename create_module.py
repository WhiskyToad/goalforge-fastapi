import os


def create_project_files(project_name: str):
    # Create main project folder
    project_path = os.path.join("app", project_name)
    os.makedirs(project_path)

    # Create files with project name prefix
    files = [
        f"{project_name}{suffix}.py"
        for suffix in ["Model", "Repository", "Routes", "Schema", "Service"]
    ]
    for filename in files:
        filepath = os.path.join(project_path, filename)
        with open(filepath, "w") as f:
            f.write("# Placeholder file")

    print(f"Project files for '{project_name}' created successfully.")


if __name__ == "__main__":
    project_name = input("Enter project name: ")
    create_project_files(project_name)
