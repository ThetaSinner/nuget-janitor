#!/usr/bin/env python3
import argparse
import os
import sys
import time

import semver
from semver import VersionInfo


def get_config():
    if len(sys.argv) < 1:
        return None

    parser = argparse.ArgumentParser(description='ding')
    parser.add_argument('--source', metavar='S', type=str, help='The package source to tidy', dest='source')
    parser.add_argument('--dry-run', action='store_true',
                        help='Do a dry run, printing the tidy plan and not taking any action')
    parser.add_argument('--remove-released', action='store_true',
                        help='Remove pre-release packages which have an associated release')
    parser.add_argument('--remove-with-later', action='store_true',
                        help='Remove pre-release packages which have been superceded by later release version')
    parser.add_argument('--remove-max-age', metavar='I', type=int,
                        help='Remove packages older than the given number days', dest='max_age')

    return parser.parse_args()


def list_subdirectories(source_dir):
    return [os.path.join(source_dir, sub_dir) for sub_dir in os.listdir(source_dir)
            if os.path.isdir(os.path.join(source_dir, sub_dir))]


def list_packages(version_dir):
    return [os.path.join(version_dir, f) for f in os.listdir(version_dir)
            if os.path.isfile(os.path.join(version_dir, f)) and os.path.splitext(f)[1] == '.nupkg']


def version_from_version_path(version_path):
    return VersionInfo.parse(os.path.basename(version_path))


def clean_up():
    config = get_config()
    if config is None:
        print("Invalid config. Try --help")
        return

    if config.dry_run:
        print("Performing dry run.")

    package_paths = list_subdirectories(config.source)
    for path in package_paths:
        clean_up_package(config, os.path.basename(path), path)


def clean_up_package(config, package_id, path):
    if config.dry_run:
        print("")
        print("")
        print("Cleaning up package with id [", package_id, "]")

    remove_versions = set()

    version_paths = list_subdirectories(path)

    versions = [version_from_version_path(ver) for ver in version_paths]
    versions.sort()

    if config.remove_released:
        versions_to_remove = find_pre_releases_with_release(versions)
        remove_versions.update(versions_to_remove)
        if config.dry_run:
            versions_to_remove = list(versions_to_remove)
            versions_to_remove.sort()
            print("Found pre-release packages with an associated release", [str(x) for x in versions_to_remove])

    if config.remove_with_later:
        versions_to_remove = find_pre_releases_with_later_release(versions)
        remove_versions.update(versions_to_remove)
        if config.dry_run:
            versions_to_remove = list(versions_to_remove)
            versions_to_remove.sort()
            print("Found pre-release packages with a later release", [str(x) for x in versions_to_remove])

    if config.max_age is not None and config.max_age > 0:
        versions_to_remove = find_old_pre_release_packages(version_paths, config.max_age * 24 * 60 * 60)
        remove_versions.update(versions_to_remove)
        if config.dry_run:
            versions_to_remove = list(versions_to_remove)
            versions_to_remove.sort()
            print("Found pre-release packages which more than", config.max_age,
                  "days old.", [str(x) for x in versions_to_remove])

    if config.dry_run:
        versions_to_remove = list(remove_versions)
        versions_to_remove.sort()
        print("Would remove package versions", [str(x) for x in versions_to_remove])
    else:
        print("Removing packages is not supported yet!")


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


def find_old_pre_release_packages(version_paths, max_age_seconds):
    versions_to_remove = []
    current_time = time.time()

    for version_path in version_paths:
        version = version_from_version_path(version_path)
        if version.prerelease is None:
            continue

        package_files = list_packages(version_path)

        if len(package_files) != 1:
            print("Invalid package identified at", version_path,
                  ". Found an invalid number of package files", package_files)
            continue

        package_modified_time = os.path.getmtime(package_files[0])

        if (current_time - package_modified_time) > max_age_seconds:
            versions_to_remove.append(version)

    return versions_to_remove


if __name__ == '__main__':
    clean_up()
