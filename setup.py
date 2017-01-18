from distutils.core import setup
setup(
    name = 'smasherstats',
    packages = ['smasherstats'],
    version = '1.3.3',
    description = 'Library for stats gathering on smash players using web scrapers',
    author = 'Michael Krasnitski',
    author_email = 'michael.krasnitski@gmail.com',
    license='MIT',
    url = 'https://github.com/PolarBearITS/smasherstats',
    download_url = 'https://github.com/PolarBearITS/smasherstats/tarball/1.3.3',
    install_requires = [
        'requests',
        'docopt',
        'beautifulsoup4',
        'pysmash'
    ]
)