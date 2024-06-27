from src.dependency_resolver import DependencyResolver


def install_packages(package_json_path, node_modules_path, specific_packages=None, visualize=True,
                     force_visualize=False):
    """
    Install packages listed in package.json or specific packages if provided.

    Args:
    package_json_path (str): Path to the package.json file
    node_modules_path (str): Path to the node_modules directory
    specific_packages (list): List of specific packages to install (optional)
    visualize (bool): Whether to visualize the dependency tree (default True)
    force_visualize (bool): Whether to force visualization even for large trees (default False)
    """
    resolver = DependencyResolver(package_json_path, node_modules_path)
    resolved_dependencies, installation_order = resolver.resolve_and_install_dependencies(
        specific_packages=specific_packages,
        visualize=(visualize or force_visualize),
        force_visualize=force_visualize
    )

    if resolved_dependencies:
        print("\nInstallation completed. Resolved dependencies:")
        for package, version in installation_order:
            print(f"{package}@{version}")
    else:
        print("No packages were installed.")


def install_command(args):
    """
    Command-line interface for the install command.

    Args:
    args (argparse.Namespace): Parsed command-line arguments
    """
    package_json_path = 'package.json'
    node_modules_path = 'node_modules'

    if args.packages:
        print(f"Installing specific packages: {', '.join(args.packages)}")
        install_packages(package_json_path, node_modules_path, specific_packages=args.packages,
                         visualize=not args.no_visualize, force_visualize=args.force_visualize)
    else:
        print("Installing all packages from package.json")
        install_packages(package_json_path, node_modules_path,
                         visualize=not args.no_visualize, force_visualize=args.force_visualize)


def setup_install_parser(subparsers):
    install_parser = subparsers.add_parser('install', help='Install packages')
    install_parser.add_argument('packages', nargs='*', help='Specific packages to install (optional)')
    install_parser.add_argument('--no-visualize', action='store_true', help='Disable dependency tree visualization')
    install_parser.add_argument('--force-visualize', action='store_true',
                                help='Force visualization even for large dependency trees')
    install_parser.set_defaults(func=install_command)
