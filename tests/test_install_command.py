import unittest
from unittest.mock import patch, MagicMock
from src.commands.install import install_packages, install_command


class TestInstallCommand(unittest.TestCase):

    @patch('src.commands.install.DependencyResolver')
    def test_install_packages(self, mock_resolver_class):
        # Setup mock
        mock_resolver = MagicMock()
        mock_resolver.resolve_and_install_dependencies.return_value = (
            {'package1': '1.0.0', 'package2': '2.0.0'},
            [('package1', '1.0.0'), ('package2', '2.0.0')]
        )
        mock_resolver_class.return_value = mock_resolver

        # Call the function
        install_packages('package.json', 'node_modules', visualize=True)

        # Assertions
        mock_resolver_class.assert_called_once_with('package.json', 'node_modules')
        mock_resolver.resolve_and_install_dependencies.assert_called_once_with(
            specific_packages=None,
            visualize=True,
            force_visualize=False
        )

    @patch('src.commands.install.install_packages')
    def test_install_command_all_packages(self, mock_install_packages):
        # Setup mock args
        args = MagicMock()
        args.packages = []
        args.no_visualize = False
        args.force_visualize = False

        # Call the function
        install_command(args)

        # Assertions
        mock_install_packages.assert_called_once_with(
            'package.json', 'node_modules',
            visualize=True, force_visualize=False
        )

    @patch('src.commands.install.install_packages')
    def test_install_command_specific_packages(self, mock_install_packages):
        # Setup mock args
        args = MagicMock()
        args.packages = ['package1', 'package2']
        args.no_visualize = True
        args.force_visualize = True

        # Call the function
        install_command(args)

        # Assertions
        mock_install_packages.assert_called_once_with(
            'package.json', 'node_modules',
            specific_packages=['package1', 'package2'],
            visualize=False, force_visualize=True
        )


if __name__ == '__main__':
    unittest.main()
