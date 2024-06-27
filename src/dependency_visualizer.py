import os


def visualize_installation_tree(node_modules_path):
    def _visualize(path, prefix=""):
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        for i, dir in enumerate(sorted(dirs)):
            is_last = i == len(dirs) - 1
            print(f"{prefix}{'└── ' if is_last else '├── '}{dir}")
            _visualize(os.path.join(path, dir), prefix + ('    ' if is_last else '│   '))

    print("Installation Tree:")
    _visualize(node_modules_path)


def visualize_dependency_tree(resolved_dependencies):
    def _visualize(package, version, depth=0, is_last=True):
        prefix = "  " * (depth - 1) + ("└── " if is_last else "├── ") if depth > 0 else ""
        print(f"{prefix}{package}@{version}")

        children = [(sub_pkg, sub_ver) for (sub_pkg, sub_ver), parents in resolved_dependencies.items() if
                    (package, version) in parents]
        for i, (sub_pkg, sub_ver) in enumerate(children):
            _visualize(sub_pkg, sub_ver, depth + 1, is_last=(i == len(children) - 1))

    print("Dependency Tree:")
    roots = [(pkg, ver) for (pkg, ver), parents in resolved_dependencies.items() if not parents]
    for i, (pkg, ver) in enumerate(roots):
        _visualize(pkg, ver, is_last=(i == len(roots) - 1))


def should_visualize(node_count, force_visualize=False):
    if node_count > 30 and not force_visualize:
        print(f"\nWarning: Large dependency tree detected ({node_count} nodes). Visualization disabled.")
        print("Use --force-visualize to override this behavior.")
        return False
    return True
