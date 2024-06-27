import semver


class MockNpmApi:
    registry = {
        'Module-A': {'1.0.0': {}, '1.1.0': {}, '2.0.0': {}},
        'Module-B': {'1.0.0': {}, '1.5.0': {}, '2.0.0': {}},
        'Module-C': {'1.0.0': {}, '1.2.0': {}, '1.3.0': {}},
        'Module-D': {'1.0.0': {}, '1.1.0': {}, '1.2.0': {}},
        'Module-E': {'1.0.0': {}, '2.0.0': {}, '2.1.0': {}}
    }

    dependencies = {
        'Module-A': {'Module-B': '^1.0.0'},
        'Module-C': {'Module-B': '^2.0.0'},
        'Module-D': {'Module-B': '^1.5.0'},
        'Module-E': {'Module-B': '~1.0.0'},
    }

    @staticmethod
    def get_latest_satisfying_version(package, version_req):
        available_versions = MockNpmApi.registry.get(package, {}).keys()
        valid_versions = [v for v in available_versions if semver.match(v, version_req)]
        return max(valid_versions, key=semver.Version.parse) if valid_versions else None

    @staticmethod
    def fetch_package_info(package, version):
        if package in MockNpmApi.dependencies:
            return {
                'version': version,
                'dependencies': MockNpmApi.dependencies[package]
            }
        return {'version': version, 'dependencies': {}}

    @staticmethod
    def download_package(package, version, path):
        # Simulate successful download
        return True
