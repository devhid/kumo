from setuptools import setup

setup(
    name='kumo',
    version='0.1',
    py_modules=['kumo'],
    install_requires=[
        'Click',
        'PyQuery',
        'tldextract'
    ],
    entry_points='''
        [console_scripts]
        kumo=kumo:main
    ''',
)