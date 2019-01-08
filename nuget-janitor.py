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

    print([str(v) for v in versions])

    print([v.prerelease for v in versions])

    find_pre_releases_with_releases(versions)

    pass


def find_pre_releases_with_releases(versions):
    for index, version in enumerate(versions):
        if version.prerelease is None:
            continue

        version_base = VersionInfo(major=version.major, minor=version.minor, patch=version.patch)

        for scanIndex, scanVersion in enumerate(versions, start=index):
            scan_version_base = VersionInfo(major=scanVersion.major, minor=scanVersion.minor, patch=scanVersion.patch)

            cmp = semver.compare(version_base, scan_version_base)
    pass


if __name__ == '__main__':
    clean_up()
