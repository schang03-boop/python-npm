import os
import json
import hashlib


class PackageValidator:
    def __init__(self, node_modules_path):
        self.node_modules_path = node_modules_path

    def verify_package_installation(self, package, version):
        package_path = os.path.join(self.node_modules_path, package)
        if not os.path.exists(package_path):
            print(f"Error: Package directory for {package}@{version} does not exist.")
            return False

        if not self._verify_package_json(package_path, package, version):
            return False

        if not self._verify_package_structure(package_path):
            return False

        if not self._verify_package_checksum(package_path, package, version):
            return False

        if not self._verify_package_dependencies(package_path):
            return False

        print(f"Package {package}@{version} verified successfully.")
        return True

    def _verify_package_json(self, package_path, expected_name, expected_version):
        package_json_path = os.path.join(package_path, 'package.json')
        if not os.path.exists(package_json_path):
            print(f"Error: package.json not found for {expected_name}@{expected_version}")
            return False

        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        if package_data.get('name') != expected_name:
            print(f"Error: Package name mismatch. Expected {expected_name}, found {package_data.get('name')}")
            return False

        if package_data.get('version') != expected_version:
            print(f"Error: Version mismatch. Expected {expected_version}, found {package_data.get('version')}")
            return False

        return True

    def _verify_package_structure(self, package_path):
        required_files = ['package.json', 'README.md', 'LICENSE']
        for file in required_files:
            if not os.path.exists(os.path.join(package_path, file)):
                print(f"Error: Required file {file} is missing.")
                return False
        return True

    def _verify_package_checksum(self, package_path, package, version):
        # In a real implementation, you would fetch the expected checksum from a trusted source
        # For this example, we'll just compute and print the checksum
        checksum = self._compute_directory_checksum(package_path)
        print(f"Computed checksum for {package}@{version}: {checksum}")
        # You would typically compare this checksum with an expected value
        return True

    def _compute_directory_checksum(self, directory):
        checksum = hashlib.md5()
        for root, dirs, files in os.walk(directory):
            for file in sorted(files):
                filepath = os.path.join(root, file)
                with open(filepath, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        checksum.update(chunk)
        return checksum.hexdigest()

    def _verify_package_dependencies(self, package_path):
        package_json_path = os.path.join(package_path, 'package.json')
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        dependencies = package_data.get('dependencies', {})
        for dep, version in dependencies.items():
            dep_path = os.path.join(package_path, 'node_modules', dep)
            if not os.path.exists(dep_path):
                print(f"Error: Dependency {dep}@{version} is missing.")
                return False
            if not self._verify_package_json(dep_path, dep, version):
                return False

        return True
