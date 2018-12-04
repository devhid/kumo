from setuptools import setup

setup(
    name='kumo',
    version='0.1',
    packages = ['','bruteforce','configs','crawler','graphs','fake-website','funcs','network', 'tests','utils'],
    package_dir = {'bruteforce':'bruteforce', 'configs':'configs', 'crawler':'crawler','fake-website': 'fake-website',
                    'funcs':'funcs', 'graphs':'graphs','network':'network', 'tests':'tests','utils':'utils'},
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