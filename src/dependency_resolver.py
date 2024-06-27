from collections import OrderedDict
import os
import time

from src.cache_manager import CacheManager
from src.lock_file_manager import LockFileManager
from src.installation_animator import InstallationAnimator
from src.package_validator import PackageValidator
import src.dependency_visualizer as visualizer
from src.utils.file_operations import create_directory, read_package_json
from src.utils.npm_api import download_package, fetch_package_info, get_latest_satisfying_version


class DependencyResolver:
    def __init__(self, package_json_path, node_modules_path):
        self.package_json_path = package_json_path
        self.node_modules_path = node_modules_path
        self.resolved_dependencies = OrderedDict()
        self.installed_packages = set()
        self.top_level_packages = OrderedDict()
        self.cache_manager = CacheManager(os.path.join(os.path.dirname(node_modules_path), '.package_cache'))
        self.lock_file_manager = LockFileManager(os.path.dirname(package_json_path))
        self.resolution_stack = set()
        self.resolution_order = []  # To maintain the order for circular dependency reporting
        self.package_validator = PackageValidator(node_modules_path)
        self.animator = InstallationAnimator()
        self.installation_order = []

    def resolve_and_install_dependencies(self, specific_packages=None, visualize=True, force_visualize=False):
        package_json = read_package_json(self.package_json_path)
        dependencies = package_json.get('dependencies', {})
        dev_dependencies = package_json.get('devDependencies', {})

        if self.lock_file_manager.is_lock_file_current(self.package_json_path) and not specific_packages:
            print("Lock file is up to date. Using locked versions.")
            locked_dependencies = self.lock_file_manager.read_lock_file()['dependencies']
            dependencies_to_install = OrderedDict(locked_dependencies)
        else:
            if specific_packages:
                dependencies_to_install = OrderedDict(
                    (pkg, dependencies.get(pkg) or dev_dependencies.get(pkg)) for pkg in specific_packages if
                    dependencies.get(pkg) or dev_dependencies.get(pkg))
                if len(dependencies_to_install) != len(specific_packages):
                    missing = [pkg for pkg in specific_packages if pkg not in dependencies_to_install]
                    print(f"Warning: The following packages are not in package.json: {', '.join(missing)}")
            else:
                dependencies_to_install = OrderedDict(dependencies)
                dependencies_to_install.update(dev_dependencies)

        self.resolve_dependencies(dependencies_to_install)
        self.install_resolved_dependencies()

        if visualize:
            node_count = self.count_tree_nodes()
            if visualizer.should_visualize(node_count, force_visualize):
                print("\nVisualization of installed packages:")
                visualizer.visualize_installation_tree(self.node_modules_path)

                print("\nVisualization of dependency tree:")
                visualizer.visualize_dependency_tree(self.resolved_dependencies)

        return self.resolved_dependencies, self.installation_order

    def resolve_dependencies(self, dependencies):
        lock_file = self.lock_file_manager.read_lock_file()
        for package, version_req in dependencies.items():
            if lock_file and package in lock_file['dependencies']:
                locked_version = lock_file['dependencies'][package]['version']
                self.resolve_package(package, locked_version, is_top_level=True, use_locked=True)
            else:
                self.resolve_package(package, version_req, is_top_level=True)

    def resolve_package(self, package, version_req, parent=None, is_top_level=False, use_locked=False):
        try:
            if use_locked:
                version = version_req
            else:
                version = get_latest_satisfying_version(package, version_req)
            key = (package, version)

            # Check for circular dependencies
            if key in self.resolution_stack:
                cycle = self.resolution_order[self.resolution_order.index(key):] + [key]
                print(f"Warning: Circular dependency detected: {' -> '.join([f'{p}@{v}' for p, v in cycle])}")
                return

            self.resolution_stack.add(key)
            self.resolution_order.append(key)

            if key not in self.resolved_dependencies:
                self.resolved_dependencies[key] = set()
                if is_top_level or package not in self.top_level_packages:
                    self.top_level_packages[package] = version

            if parent:
                self.resolved_dependencies[key].add(parent)

            # Fetch package info to get its dependencies
            package_info = fetch_package_info(package, version)
            sub_dependencies = package_info.get('dependencies', {})

            # Recursively resolve sub-dependencies
            for sub_package, sub_version_req in sub_dependencies.items():
                self.resolve_package(sub_package, sub_version_req, parent=key)

            self.resolution_stack.remove(key)
            self.resolution_order.pop()

        except Exception as e:
            print(f"Error resolving {package}@{version_req}: {str(e)}")
            if key in self.resolution_stack:
                self.resolution_stack.remove(key)
            if self.resolution_order and self.resolution_order[-1] == key:
                self.resolution_order.pop()

    def install_resolved_dependencies(self):
        create_directory(self.node_modules_path)

        packages_to_install = [
            (package, version)
            for (package, version), parents in self.resolved_dependencies.items()
            if (package, version) not in self.installed_packages
        ]

        start_time = time.time()
        self.animator.animate_installation(packages_to_install)

        for package, version in packages_to_install:
            if package in self.top_level_packages and self.top_level_packages[package] == version:
                self.install_package(package, version, self.node_modules_path)
            else:
                for parent in self.resolved_dependencies[(package, version)]:
                    parent_path = os.path.join(self.node_modules_path, *parent[0].split('/'))
                    self.install_package(package, version, os.path.join(parent_path, 'node_modules'))

        total_time = time.time() - start_time
        self.animator.show_final_message(len(packages_to_install), total_time)

        # Update lock file after installation
        self.lock_file_manager.write_lock_file(self.resolved_dependencies)

    def install_package(self, package, version, install_path):
        package_install_path = os.path.join(install_path, package)
        if (package, version) not in self.installed_packages:
            cached_path = self.cache_manager.get_cached_package(package, version)
            if cached_path:
                print(f"Installing {package}@{version} from cache")
                os.makedirs(os.path.dirname(package_install_path), exist_ok=True)
                os.symlink(cached_path, package_install_path)
                self.installed_packages.add((package, version))
            elif download_package(package, version, package_install_path):
                print(f"Successfully installed {package}@{version} in {install_path}")
                self.installed_packages.add((package, version))
                # Cache the newly downloaded package
                self.cache_manager.cache_package(package, version, package_install_path)
            else:
                print(f"Failed to install {package}@{version}")
                return False

            # Verify the installation
            if not self.package_validator.verify_package_installation(package, version):
                print(f"Warning: Verification failed for {package}@{version}")
                # You might want to implement some recovery or cleanup logic here
                return False

            self.installation_order.append((package, version))

        return True

    def count_tree_nodes(self):
        return len(self.resolved_dependencies)
