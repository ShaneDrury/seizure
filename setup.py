from setuptools import setup

setup(
    name='seizure',
    version='1.0',
    packages=['seizure', 'seizure.lib'],
    license='',
    author='Shane Drury',
    author_email='shane.r.drury@gmail.com',
    description='Download VODs from Twitch',
    entry_points={'console_scripts': ['seizure = seizure.scripts:main'], },
    keywords=['twitch', 'vod', 'download'],
    url='https://github.com/ShaneDrury/seizure',
    download_url='https://github.com/ShaneDrury/seizure/tarball/1.0',
    install_requires=['requests >= 2.5, < 2.6',
                      'progressbar2 >= 2.7 < 2.8'],
    )
