from setuptools import setup

setup(
    name='kumo',
    version='0.1',
    packages = ['','bruteforce','configs','fake-website','funcs','network'],
    package_dir = {'bruteforce':'bruteforce', 'configs':'configs', 'fake-website': 'fake-website',
                    'funcs':'funcs', 'network':'network'},
    install_requires=[
        'Click',
        'PyQuery',
        'urllib3',
        'tldextract'
    ],
    entry_points='''
        [console_scripts]
        kumo=kumo:main
    ''',
)