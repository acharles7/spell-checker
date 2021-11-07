from setuptools import setup

INSTALL_REQUIRES = []

setup(
    packages=["spell"],
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["spell_check=spell.main:main",]},
)
