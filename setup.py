from setuptools import setup, find_packages

setup(
    name="strava_data_analyser",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "contourpy==1.3.0",
        "cycler==0.12.1",
        "dnspython==2.7.0",
        "exceptiongroup==1.2.2",
        "fonttools==4.56.0",
        "idna==3.10",
        "importlib_resources==6.5.2",
        "iniconfig==2.0.0",
        "kiwisolver==1.4.7",
        "matplotlib==3.9.4",
        "numpy==2.0.2",
        "packaging==24.2",
        "pandas==2.2.3",
        "pillow==11.1.0",
        "pluggy==1.5.0",
        "polars==1.27.1",
        "pymongo==4.11.2",
        "pyparsing==3.2.1",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "pytz==2025.1",
        "requests==2.32.3",
        "six==1.17.0",
        "tomli==2.2.1",
        "tzdata==2025.1",
        "urllib3==2.3.0",
        "zipp==3.21.0"
    ],
    extras_require={
        "test": [
            "pytest==8.3.5"
        ]
    }
)
