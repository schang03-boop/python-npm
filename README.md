# Python NPM-like Package Manager

A lightweight, NPM-inspired package manager implemented in Python. This project aims to provide a simple yet effective way to manage dependencies in NodeJS projects, mimicking some of the core functionalities of Node.js's NPM.

## Features

- 📦 Dependency resolution and installation
- 🔒 Lock file support for deterministic builds
- 🚀 Efficient caching mechanism
- 🌳 Visualization of dependency trees
- 🔄 Circular dependency detection
- ✅ Package integrity validation

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/schang03-boop/python-npm.git
   cd python-npm
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the package manager:
   ```
   python main.py install
   ```

## Usage

- Add a package:
  ```
  python main.py add package-name
  ```

- Install all dependencies:
  ```
  python main.py install
  ```

- Visualize dependency tree:
  ```
  python main.py install --visualize
  ```

## Project Structure

```
python-npm/
├── src/
│   ├── dependency_resolver.py
│   ├── cache_manager.py
│   ├── package_manager.py
│   ├── cli.py
│   ├── lock_file_manager.py
│   ├── package_validator.py
│   ├── installation_animator.py
│   └── utils/
│       ├── npm_api.py
│       └── file_operations.py
├── tests/
│   ├── test_dependency_resolver.py
│   ├── mock_npm_api.py
│   └── mock_file_operations.py
├── main.py
├── requirements.txt
├── LICENSE
├── setup.py
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Node.js's NPM
- Built with love and Python 🐍❤️