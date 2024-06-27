import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from src.dependency_resolver import DependencyResolver
from tests.mock_npm_api import MockNpmApi
from tests.mock_file_operations import MockFileOperations


class TestDependencyResolver(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_project'
        os.makedirs(self.test_dir, exist_ok=True)
        self.package_json_path = os.path.join(self.test_dir, 'package.json')
        self.node_modules_path = os.path.join(self.test_dir, 'node_modules')
        self.lock_file_path = os.path.join(self.test_dir, 'package-lock.json')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('src.dependency_resolver.get_latest_satisfying_version', MockNpmApi.get_latest_satisfying_version)
    @patch('src.dependency_resolver.fetch_package_info', MockNpmApi.fetch_package_info)
    @patch('src.dependency_resolver.download_package', MockNpmApi.download_package)
    @patch('src.dependency_resolver.create_directory', MockFileOperations.create_directory)
    @patch('src.dependency_resolver.read_package_json', MockFileOperations.read_package_json)
    @patch('src.dependency_resolver.write_package_json', MockFileOperations.write_package_json)
    @patch('src.dependency_resolver.LockFileManager.read_lock_file', MockFileOperations.read_lock_file)
    @patch('src.dependency_resolver.LockFileManager.write_lock_file', MockFileOperations.write_lock_file)
    def test_resolve_and_install_dependencies(self):
        mock_lock_file_manager = MagicMock()
        mock_lock_file_manager.is_lock_file_current.return_value = False
        mock_lock_file_manager.read_lock_file.return_value = None

        resolver = DependencyResolver(self.package_json_path, self.node_modules_path)
        resolver.lock_file_manager = mock_lock_file_manager

        resolved_dependencies, installation_order = resolver.resolve_and_install_dependencies(visualize=False)

        # Check if all expected modules are in resolved_dependencies
        expected_modules = ['Module-A', 'Module-B', 'Module-C', 'Module-D', 'Module-E']
        for module in expected_modules:
            self.assertTrue(any(module in key for key in resolved_dependencies.keys()))

        # Check if Module-B has two different versions
        module_b_versions = [ver for pkg, ver in resolved_dependencies.keys() if pkg == 'Module-B']
        self.assertEqual(len(set(module_b_versions)), 2)

        # Check dependencies
        self.assertIn(('Module-A', '2.0.0'), resolved_dependencies[('Module-B', '1.5.0')])
        self.assertIn(('Module-E', '2.1.0'), resolved_dependencies[('Module-B', '1.0.0')])
        self.assertIn(('Module-C', '1.3.0'), resolved_dependencies[('Module-B', '2.0.0')])
        self.assertIn(('Module-D', '1.2.0'), resolved_dependencies[('Module-B', '1.5.0')])

        # Check if lock file was written
        mock_lock_file_manager.write_lock_file.assert_called_once()

        # Check installation order
        self.assertEqual(len(installation_order), len(resolved_dependencies))
        for package, version in installation_order:
            self.assertIn((package, version), resolved_dependencies)

    @patch('src.dependency_resolver.read_package_json', MockFileOperations.read_package_json)
    @patch('src.dependency_resolver.LockFileManager.read_lock_file', MockFileOperations.read_lock_file)
    def test_use_lock_file(self):
        mock_lock_file_manager = MagicMock()
        mock_lock_file_manager.is_lock_file_current.return_value = True
        mock_lock_file_manager.read_lock_file.return_value = {
            'dependencies': {
                'Module-A': {'version': '1.1.0', 'dependencies': {'Module-B': '1.0.0'}},
                'Module-B': {'version': '1.0.0', 'dependencies': {}},
                'Module-C': {'version': '1.2.0', 'dependencies': {'Module-B': '2.0.0'}},
                'Module-D': {'version': '1.1.0', 'dependencies': {'Module-B': '1.5.0'}},
                'Module-E': {'version': '2.0.0', 'dependencies': {'Module-B': '1.0.0'}}
            }
        }

        resolver = DependencyResolver(self.package_json_path, self.node_modules_path)
        resolver.lock_file_manager = mock_lock_file_manager

        resolved_dependencies, installation_order = resolver.resolve_and_install_dependencies(visualize=False)

        # Check if resolved dependencies match lock file
        expected_deps = mock_lock_file_manager.read_lock_file()['dependencies']
        for module, info in expected_deps.items():
            self.assertIn((module, info['version']), resolved_dependencies)

        # Check if lock file was not written (as it was already up-to-date)
        mock_lock_file_manager.write_lock_file.assert_not_called()

        # Check installation order
        self.assertEqual(len(installation_order), len(resolved_dependencies))
        for package, version in installation_order:
            self.assertIn((package, version), resolved_dependencies)

    @patch('src.dependency_resolver.get_latest_satisfying_version', MockNpmApi.get_latest_satisfying_version)
    @patch('src.dependency_resolver.fetch_package_info', MockNpmApi.fetch_package_info)
    @patch('src.dependency_resolver.download_package', MockNpmApi.download_package)
    @patch('src.dependency_resolver.create_directory', MockFileOperations.create_directory)
    @patch('src.dependency_resolver.read_package_json', MockFileOperations.read_package_json)
    @patch('src.dependency_resolver.write_package_json', MockFileOperations.write_package_json)
    @patch('src.dependency_resolver.LockFileManager.read_lock_file', MockFileOperations.read_lock_file)
    @patch('src.dependency_resolver.LockFileManager.write_lock_file', MockFileOperations.write_lock_file)
    def test_circular_dependency_detection(self):
        # Mock a circular dependency scenario
        def mock_fetch_package_info(package, version):
            dependencies = {
                'Module-A': {'dependencies': {'Module-B': '^1.0.0'}},
                'Module-B': {'dependencies': {'Module-C': '^1.0.0'}},
                'Module-C': {'dependencies': {'Module-A': '^1.0.0'}}
            }
            return {'version': version, 'dependencies': dependencies.get(package, {})}

        with patch('src.dependency_resolver.fetch_package_info', mock_fetch_package_info):
            resolver = DependencyResolver(self.package_json_path, self.node_modules_path)
            resolved_dependencies, installation_order = resolver.resolve_and_install_dependencies(visualize=False)

            # Check if the circular dependency was detected and handled
            self.assertIn(('Module-A', '2.0.0'), resolved_dependencies)
            self.assertIn(('Module-B', '2.0.0'), resolved_dependencies)
            self.assertIn(('Module-C', '1.3.0'), resolved_dependencies)

            # The circular dependency should not cause an infinite loop
            self.assertLessEqual(len(installation_order), 3)


if __name__ == '__main__':
    unittest.main()
