from setuptools import find_packages, setup

setup(
    name='mypythonlib',
    packages=find_packages(),
    version='0.0.2',
    description='My first Python library',
    author='Me',
    install_requires=[],
    extras_require={
        "dev": [
            "pytest-runner",
            "pytest==7.0"
            "twine==6.1.0"
        ],
    },
    python_requires=">=3.13.3",
)