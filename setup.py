from setuptools import setup

setup(
    name='seizure',
    version='1.0.1',
    packages=['seizure', 'seizure.lib'],
    license='',
    author='Shane Drury',
    author_email='shane.r.drury@gmail.com',
    description='Download VODs from Twitch',
    entry_points={'console_scripts': ['seizure = seizure.scripts:main'], },
    keywords=['twitch', 'vod', 'download'],
    url='https://github.com/ShaneDrury/seizure',
    download_url='https://github.com/ShaneDrury/seizure/tarball/1.0.1',
    install_requires=['requests', 'progressbar'],
    )
