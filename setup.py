from setuptools import setup
import re

requirements = [
    "aiohttp"
]

with open('pycordia/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if version:
        version = version.group(1)
    else:
        version = ""

with open('README.md', "r", encoding="utf-8-sig") as f:
    readme = f.read()

setup(name='pycordia',
      author='Angel Carias',
      url='https://github.com/angelCarias/pycordia',
      version=version,
      packages=["pycordia", "pycordia/models", "pycordia/errors"],
      license='MIT',
      description='The Discord bot framework for Python',
      long_description=readme,
      long_description_content_type="text/markdown",
      install_requires=requirements,
      python_requires='>=3.7.0',
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
      ]
)
