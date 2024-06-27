import os
import hashlib
import shutil


class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_path(self, package_name, version):
        cache_key = f"{package_name}@{version}"
        return os.path.join(self.cache_dir, hashlib.md5(cache_key.encode()).hexdigest())

    def is_cached(self, package_name, version):
        cache_path = self.get_cache_path(package_name, version)
        return os.path.exists(cache_path)

    def get_cached_package(self, package_name, version):
        cache_path = self.get_cache_path(package_name, version)
        if self.is_cached(package_name, version):
            return cache_path
        return None

    def cache_package(self, package_name, version, package_path):
        cache_path = self.get_cache_path(package_name, version)
        shutil.copytree(package_path, cache_path)

    def clear_cache(self):
        shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
