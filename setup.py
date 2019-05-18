import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    author='Josiah Bradley',
    author_email='Josiah Bradley@gmail.com',
    name="mod-or-die",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'play = levels.level_01:main',
        ]
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)