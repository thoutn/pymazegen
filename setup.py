from setuptools import setup, find_packages


setup(
    name='pymazegen',
    version='0.1.0',
    description='A maze generator amd visualiser',
    author='Tamas Nagy (aka thoutn)',
    url='https://github.com/thoutn/pymazegen.git',
    license='MIT License',
    install_requires=['numpy', 'pillow'],
    package_dir={'pymazegen': 'src/pymazegen'},
    packages=find_packages(where='src')
)
