from setuptools import setup, find_packages
setup(
    name="KivyTiledRPG",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': ['collision-editor = kivytiledrpg.helpers.collision_editor.main:main']}
)