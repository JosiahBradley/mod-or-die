import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

data_files = []
for root, dirs, files in os.walk('src/mod_or_die/resources/arcade'):
    ff = []
    for file in files:
        ff.append(os.path.join(root, file))
    data_files.append((root, ff))

setuptools.setup(
    author='Josiah Bradley',
    author_email='Josiah Bradley@gmail.com',
    name="mod-or-die",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'play = mod_or_die.levels.level_01:main',
        ]
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    data_files=data_files,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)
