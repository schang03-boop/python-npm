import os
import json


class MockFileOperations:
    @staticmethod
    def create_directory(path):
        # In a real test, you might use a temporary directory
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def read_package_json(path):
        # Return a mock package.json content
        return {
            'dependencies': {
                'Module-A': '^1.0.0',
                'Module-C': '^1.0.0',
                'Module-D': '^1.0.0',
                'Module-E': '^2.0.0'
            }
        }

    @staticmethod
    def write_package_json(path, content):
        # In a real test, you might write to a temporary file
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)

    @staticmethod
    def read_lock_file(path):
        # If the lock file doesn't exist, return None
        if not os.path.exists(path):
            return None

        # If it exists, read and return its content
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def write_lock_file(path, content):
        # Write the lock file content
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)

    @staticmethod
    def file_exists(path):
        return os.path.exists(path)