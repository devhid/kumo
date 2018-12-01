from setuptools import setup, find_packages

setup(
    name='kumo',
    version='0.1',
    packages=find_packages(),
    py_modules=['kumo'],
    install_requires=[
        'Click',
        'PyQuery',
        'urllib3',
    ],
    entry_points='''
        [console_scripts]
        kumo=kumo:main
    ''',
)