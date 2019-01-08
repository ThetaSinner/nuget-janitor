#!/usr/bin/env python3
import argparse
import os
import sys

import semver
from semver import VersionInfo


def get_config():
    if len(sys.argv) < 1:
        return None

    parser = argparse.ArgumentParser(description='ding')
    parser.add_argument('-Source', metavar='S', type=str, help='The package source to tidy', dest='source')

    return parser.parse_args()


def list_subdirectories(source_dir):
    return [os.path.join(source_dir, sub_dir) for sub_dir in os.listdir(source_dir)
            if os.path.isdir(os.path.join(source_dir, sub_dir))]


def clean_up():
    config = get_config()
    if config is None:
        print("Invalid config. Try --help")

    package_paths = list_subdirectories(config.source)
    for path in package_paths:
        clean_up_package(os.path.basename(path), path)


def clean_up_package(package_id, path):
    version_paths = list_subdirectories(path)

    versions = [VersionInfo.parse(os.path.basename(ver)) for ver in version_paths]
    versions.sort()

    versions_to_remove = find_pre_releases_with_release(versions)

    print("Time to remove these pretties!")
    print([str(x) for x in versions_to_remove])

    versions_to_remove = find_pre_releases_with_later_release(versions)

    print([str(x) for x in versions_to_remove])


def find_pre_releases_with_release(versions):
    versions_to_remove = set()

    for index, version in enumerate(versions):
        if version.prerelease is None:
            continue

        version_base = VersionInfo(major=version.major, minor=version.minor, patch=version.patch)

        if version_base not in versions:
            continue

        release_version_index = versions.index(version_base)

        versions_to_remove.update(versions[index:release_version_index])

    return versions_to_remove


def find_pre_releases_with_later_release(versions):
    versions_to_remove = set()

    base_versions = [str(VersionInfo(major=version.major, minor=version.minor, patch=version.patch))
                     for version in versions]

    for index, version in enumerate(versions):
        if version.prerelease is None:
            continue

        version_base = str(VersionInfo(major=version.major, minor=version.minor, patch=version.patch))

        release_version_index = -1
        for bv_index, bv in enumerate(base_versions):
            if semver.compare(version_base, bv) == -1 or version_base == str(versions[bv_index]):
                release_version_index = bv_index
                break

        if release_version_index == -1:
            continue

        versions_to_remove.update(versions[index:release_version_index])

    return versions_to_remove


if __name__ == '__main__':
    clean_up()
