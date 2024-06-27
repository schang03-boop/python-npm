import argparse
import os
from src.package_manager import BasicNodeJSPackageManager
from src.commands.add import setup_add_parser
from src.commands.install import setup_install_parser


def main():
    parser = argparse.ArgumentParser(description='Basic NodeJS Package Manager')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    setup_add_parser(subparsers)
    setup_install_parser(subparsers)

    args = parser.parse_args()

    # Create an instance of BasicNodeJSPackageManager
    manager = BasicNodeJSPackageManager(project_root=os.getcwd())

    if args.command == 'add':
        if args.packages:
            for package in args.packages:
                manager.add(package, dev=args.dev)
        else:
            print("Error: No packages specified for add command.")
    elif args.command == 'install':
        manager.install(visualize=not args.no_visualize, force_visualize=args.force_visualize)
    elif args.command:
        print(f"Error: Unknown command '{args.command}'")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
