from setuptools import setup, find_namespace_packages

setup(
    name='santashelper',
    version='1.0.2',
    description="console Santa's helper elf",
    url='https://github.com/kk-goit/projector',
    author='joBounty',
    author_email='kkondor@yahoo.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['asciimatics'],
    include_package_data=True,
    entry_points={'console_scripts': ['elf = santashelper.elf:main']}
) 
