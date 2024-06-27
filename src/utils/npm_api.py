import requests
import semver

NPM_REGISTRY_URL = 'https://registry.npmjs.org'


def fetch_package_info(package_name, version='latest'):
    url = f"{NPM_REGISTRY_URL}/{package_name}/{version}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_package_versions(package_name):
    url = f"{NPM_REGISTRY_URL}/{package_name}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return list(data['versions'].keys())


def parse_package_name(package_string):
    if '@' in package_string:
        name, version = package_string.rsplit('@', 1)
        return name, version
    else:
        return package_string, 'latest'


def is_version_satisfied(required_version, available_version):
    try:
        if required_version == 'latest':
            return True
        if required_version.startswith('^') or required_version.startswith('~'):
            return semver.match(available_version, required_version)
        return semver.compare(available_version, required_version) >= 0
    except ValueError:
        # If versions are not valid semver, fall back to string comparison
        return available_version == required_version


def get_latest_satisfying_version(package_name, version_requirement):
    versions = get_package_versions(package_name)
    satisfying_versions = [v for v in versions if is_version_satisfied(version_requirement, v)]
    if not satisfying_versions:
        raise ValueError(f"No version satisfying {version_requirement} found for {package_name}")
    return max(satisfying_versions, key=semver.Version.parse)


def download_package(package_name, version, target_dir):
    info = fetch_package_info(package_name, version)
    tarball_url = info['dist']['tarball']

    response = requests.get(tarball_url)
    response.raise_for_status()

    # Implementation of download and extraction...
    # (This part would involve writing the tarball to disk and extracting it)
    print(f"Downloading {package_name}@{version} to {target_dir}")
    # For now, we'll just pretend we've downloaded and extracted the package
    return True
