import os
from src.commands.add import add_package
from src.commands.install import install_packages
from src.utils.file_operations import read_package_json, write_package_json


class BasicNodeJSPackageManager:
    def __init__(self, project_root='.'):
        self.project_root = project_root
        self.package_json_path = os.path.join(project_root, 'package.json')
        self.node_modules_path = os.path.join(project_root, 'node_modules')

    def add(self, *packages, dev=False):
        """
        Add one or more packages to package.json and install them.

        Args:
        *packages (str): Package names and optional versions (e.g., 'package@1.0.0')
        dev (bool): If True, add to devDependencies instead of dependencies
        """
        for package_string in packages:
            add_package(package_string, self.package_json_path, self.node_modules_path, dev)

    def install(self):
        """
        Install all packages listed in package.json.
        """
        install_packages(self.package_json_path, self.node_modules_path)

    def remove(self, package_name):
        """
        Remove a package from package.json and node_modules.

        Args:
        package_name (str): Name of the package to remove
        """
        # Read package.json
        package_json = read_package_json(self.package_json_path)

        # Remove package from dependencies if it exists
        if 'dependencies' in package_json and package_name in package_json['dependencies']:
            del package_json['dependencies'][package_name]
            write_package_json(self.package_json_path, package_json)
            print(f"Removed {package_name} from package.json")
        else:
            print(f"{package_name} not found in package.json")

        # Remove package directory from node_modules
        package_dir = os.path.join(self.node_modules_path, package_name)
        if os.path.exists(package_dir):
            import shutil
            shutil.rmtree(package_dir)
            print(f"Removed {package_name} from node_modules")
        else:
            print(f"{package_name} not found in node_modules")

    def list_packages(self):
        """
        List all installed packages and their versions.
        """
        package_json = read_package_json(self.package_json_path)
        dependencies = package_json.get('dependencies', {})

        if dependencies:
            print("Installed packages:")
            for package, version in dependencies.items():
                print(f"{package}@{version}")
        else:
            print("No packages installed.")

    def update(self, package_name=None):
        """
        Update all packages or a specific package to their latest versions.

        Args:
        package_name (str, optional): Name of the package to update. If None, update all packages.
        """
        from src.utils.npm_api import fetch_package_info

        package_json = read_package_json(self.package_json_path)
        dependencies = package_json.get('dependencies', {})

        if package_name:
            if package_name in dependencies:
                latest_info = fetch_package_info(package_name)
                latest_version = latest_info['version']
                dependencies[package_name] = latest_version
                print(f"Updated {package_name} to version {latest_version}")
            else:
                print(f"{package_name} not found in package.json")
        else:
            for pkg in dependencies:
                latest_info = fetch_package_info(pkg)
                latest_version = latest_info['version']
                dependencies[pkg] = latest_version
                print(f"Updated {pkg} to version {latest_version}")

        package_json['dependencies'] = dependencies
        write_package_json(self.package_json_path, package_json)
        print("Don't forget to run 'install' to apply the updates.")

    def init(self):
        """
        Initialize a new package.json file.
        """
        if os.path.exists(self.package_json_path):
            print("package.json already exists.")
            return

        package_json = {
            "name": os.path.basename(os.path.abspath(self.project_root)),
            "version": "1.0.0",
            "description": "",
            "main": "index.js",
            "scripts": {
                "test": "echo \"Error: no test specified\" && exit 1"
            },
            "keywords": [],
            "author": "",
            "license": "ISC",
            "dependencies": {}
        }

        write_package_json(self.package_json_path, package_json)
        print("Initialized package.json")
