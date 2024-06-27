import argparse
import os
from src.dependency_resolver import DependencyResolver
from src.utils.file_operations import read_package_json, write_package_json


def main():
    parser = argparse.ArgumentParser(description="PyDep: Python Dependency Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize a new project")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a package to dependencies")
    parser_add.add_argument("package", help="Package to add")
    parser_add.add_argument("--dev", action="store_true", help="Add as a development dependency")

    # Install command
    parser_install = subparsers.add_parser("install", help="Install dependencies")
    parser_install.add_argument("--visualize", action="store_true", help="Visualize dependency tree")

    # Update command
    parser_update = subparsers.add_parser("update", help="Update a package")
    parser_update.add_argument("package", help="Package to update")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a package")
    parser_remove.add_argument("package", help="Package to remove")

    args = parser.parse_args()

    if args.command == "init":
        initialize_project()
    elif args.command == "add":
        add_package(args.package, args.dev)
    elif args.command == "install":
        install_dependencies(args.visualize)
    elif args.command == "update":
        update_package(args.package)
    elif args.command == "remove":
        remove_package(args.package)
    else:
        parser.print_help()


def initialize_project():
    print("Initializing new project...")
    if os.path.exists('package.json'):
        print("Project already initialized. package.json file exists.")
        return

    project_name = input("Enter project name: ")
    project_version = input("Enter project version (default 0.1.0): ") or "0.1.0"

    package_json = {
        "name": project_name,
        "version": project_version,
        "dependencies": {},
        "devDependencies": {}
    }

    write_package_json('package.json', package_json)
    print("Project initialized. Created package.json file.")


def add_package(package, is_dev):
    print(f"Adding package: {package} {'(dev)' if is_dev else ''}")
    package_json = read_package_json('package.json')

    if is_dev:
        package_json.setdefault('devDependencies', {})[package] = "*"
    else:
        package_json.setdefault('dependencies', {})[package] = "*"

    write_package_json('package.json', package_json)
    print(f"Added {package} to {'devDependencies' if is_dev else 'dependencies'} in package.json")


def install_dependencies(visualize):
    print("Installing dependencies...")
    package_json_path = 'package.json'
    node_modules_path = 'node_modules'

    if not os.path.exists(package_json_path):
        print("Error: package.json not found. Run 'pydep init' to initialize the project.")
        return

    resolver = DependencyResolver(package_json_path, node_modules_path)
    resolved_deps, install_order = resolver.resolve_and_install_dependencies(visualize=visualize)
    print(f"Installed {len(install_order)} packages")


def update_package(package):
    print(f"Updating package: {package}")
    package_json = read_package_json('package.json')

    if package in package_json.get('dependencies', {}):
        package_json['dependencies'][package] = "*"
    elif package in package_json.get('devDependencies', {}):
        package_json['devDependencies'][package] = "*"
    else:
        print(f"Package {package} not found in dependencies.")
        return

    write_package_json('package.json', package_json)
    print(f"Updated {package} in package.json. Run 'pydep install' to update the installation.")


def remove_package(package):
    print(f"Removing package: {package}")
    package_json = read_package_json('package.json')

    if package in package_json.get('dependencies', {}):
        del package_json['dependencies'][package]
    elif package in package_json.get('devDependencies', {}):
        del package_json['devDependencies'][package]
    else:
        print(f"Package {package} not found in dependencies.")
        return

    write_package_json('package.json', package_json)
    print(f"Removed {package} from package.json. Run 'pydep install' to update the installation.")


if __name__ == "__main__":
    main()