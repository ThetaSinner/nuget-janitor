from setuptools import setup

setup(
    name='nugetjanitor',
    version='1.0.0',
    packages=['nugetjanitor'],
    url='https://github.com/ThetaSinner/nuget-janitor',
    license=' GPL-3.0',
    author='ThetaSinner',
    author_email='',
    scripts=['bin/nugetjanitor'],
    description='Helper for cleaning a NuGet package repository on a file share.'
)
