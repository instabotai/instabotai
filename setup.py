from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='instabotai',
    version='1.50.00',
    description='Instagram bot scripts for promotion and API python wrapper.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Steffan Jensen',
    author_email='6hourapp@gmail.com',
    license='Apache Software License 2.0',

    url='https://github.com/instagrambot/instabotai',
    keywords=['instagram', 'bot', 'api', 'wrapper'],
    install_requires=[
        'tqdm>=4.30.0',
        'instabot',
        'tensorflow==2.0.0rc0',
        'flask',
        'opencv-python',
        'requests_toolbelt'
    ],
    entry_points={
        'console_scripts': ['instabotai=instabotai:main'],
    },
    classifiers=[
        # How mature is this project? Common values are
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Information Technology',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
)

