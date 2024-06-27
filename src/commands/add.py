import os

from src.utils.npm_api import parse_package_name, get_latest_satisfying_version
from src.utils.file_operations import read_package_json, write_package_json


def add_package(package_string, package_json_path, dev=False):
    """
    Add a package to the project's package.json file.

    Args:
    package_string (str): Package name and optional version (e.g., 'package@1.0.0')
    package_json_path (str): Path to the package.json file
    dev (bool): If True, add to devDependencies instead of dependencies
    """
    if not os.path.exists(package_json_path):
        print(f"Error: {package_json_path} not found. Please run 'npm init' to create a package.json file.")
        return

    package_name, specified_version = parse_package_name(package_string)

    try:
        if specified_version:
            version = specified_version
        else:
            version = get_latest_satisfying_version(package_name, 'latest')
    except Exception as e:
        print(f"Error fetching package info: {e}")
        return

    package_json = read_package_json(package_json_path)

    dep_type = 'devDependencies' if dev else 'dependencies'
    if dep_type not in package_json:
        package_json[dep_type] = {}

    package_json[dep_type][package_name] = version

    write_package_json(package_json_path, package_json)

    print(f"Added {package_name}@{version} to {dep_type} in package.json")


def add_command(args):
    """
    Command-line interface for the add command.

    Args:
    args (argparse.Namespace): Parsed command-line arguments
    """
    if not args.packages:
        print("Error: At least one package name is required.")
        return

    for package in args.packages:
        add_package(package, 'package.json', 'node_modules', dev=args.dev)


def setup_add_parser(subparsers):
    add_parser = subparsers.add_parser('add', help='Add package(s) to package.json.')
    add_parser.add_argument('packages', nargs='+', help='Package name(s) and optional version(s) (e.g., package@1.0.0)')
    add_parser.add_argument('--dev', action='store_true', help='Add package(s) to devDependencies')
    add_parser.set_defaults(func=add_command)
