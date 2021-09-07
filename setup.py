from setuptools import setup
import re

requirements = [
    "aiohttp"
]

with open('pycordia/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md') as f:
    readme = f.read()

setup(name='pycordia',
      author='Angel Carias',
      url='https://github.com/angelCarias/pycordia',
      version=version,
      packages=["pycordia", "pycordia/models"],
      license='MIT',
      description='A wrapper around the Discord HTTP API and WebSockets',
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
        "Programming Language :: Python :: 3.9"
      ]
)
