from setuptools import find_packages, setup

setup(
    name='HoMeNu',
    version='3.0.200206',
    author="David.SC",
    author_email="david_sc@mail.com",
    description="Home Menu",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
