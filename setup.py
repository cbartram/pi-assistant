import re
import toml
import codecs
import os.path
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def read(*parts):
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_path):
    """
      Locates the version parameters specified in an arbitrary file.
      :param file_path: List of file paths to locate the __version__ i.e find_version(package, subpackage, __init__.py)
      :return: String the semantic version like 0.0.1
      """
    version_file = read(*file_path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)

    if version_match:
        return version_match.group(1)
    raise RuntimeError(f"Unable to find version string in file: {file_path}")


def get_install_requirements():
    """
      Installs and reads the direct dependencies specified within the Pipfil. This ensures all dependencies are managed through pipenv
      and there is no need for a requirements.txt file (or multiple files to manage project dependencies)
      :return: List of package names and their required versions
      """
    try:
        with open('Pipfile', 'r') as fh:
            pipfile = fh.read()
        pipfile_toml = toml.loads(pipfile)
    except FileNotFoundError:
        return []

    try:
        required_packages = pipfile_toml['packages'].items()
    except KeyError:
        return []

    # If a version /range is specified in the Pipfile honor it
    # otherwise just list it as a package
    final_package_list = []
    for pkg, ver in required_packages:
        if isinstance(ver, dict):
            # Assuming this package is from a VCS like Github
            final_package_list.append(f"{pkg}@git+{ver['git']}#egg={pkg}")
        else:
            final_package_list.append("{0}{1}".format(pkg, ver) if ver != "*" else pkg)
    return final_package_list


setup(name='pi-assistant',
      version=find_version("pi_assistant", "__init__.py"),
      description='Raspberry Pi voice controlled smart home assistant.',
      author='Christian Bartram',
      author_email='cbartram3@gmail.com',
      scripts=[],
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*', 'test',
                                      'tests/*', 'test/*', '*.test.*', '*.test']),
      include_package_data=True,
      install_requires=get_install_requirements(),
      entry_points={
          'console_scripts': ['pi-assistant = pi_assistant.__init__:main']
      },
      tests_require=['coverage'],
      zip_safe=False
      )
