import json
import os


class LockFileManager:
    def __init__(self, project_root):
        self.lock_file_path = os.path.join(project_root, 'package-lock.json')

    def read_lock_file(self):
        if os.path.exists(self.lock_file_path):
            with open(self.lock_file_path, 'r') as f:
                return json.load(f)
        return None

    def write_lock_file(self, resolved_dependencies):
        lock_data = {
            "dependencies": {}
        }
        for package, info in resolved_dependencies.items():
            lock_data["dependencies"][package] = {
                "version": info["version"],
                "dependencies": info.get("dependencies", {})
            }

        with open(self.lock_file_path, 'w') as f:
            json.dump(lock_data, f, indent=2)

    def is_lock_file_current(self, package_json_path):
        if not os.path.exists(self.lock_file_path):
            return False

        lock_data = self.read_lock_file()
        with open(package_json_path, 'r') as f:
            package_json = json.load(f)

        for package, version in package_json.get('dependencies', {}).items():
            if package not in lock_data['dependencies'] or lock_data['dependencies'][package]['version'] != version:
                return False

        return True
