import setuptools

setuptools.setup(
    name='nugetjanitor',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=['semver>=2.8.1'],
    url='https://github.com/ThetaSinner/nuget-janitor',
    license=' GPL-3.0',
    author='ThetaSinner',
    author_email='greatdjonfire@hotmail.co.uk',
    scripts=['bin/nugetjanitor'],
    description='Helper for cleaning a NuGet package repository on a file share.'
)
