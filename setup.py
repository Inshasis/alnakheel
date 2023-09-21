from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in alnakheel/__init__.py
from alnakheel import __version__ as version

setup(
	name="alnakheel",
	version=version,
	description="for KSA client",
	author="Hidayat Ali",
	author_email="hidayatmanusiya1@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
