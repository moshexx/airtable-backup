# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="airtable-backup",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated backup tool for Airtable databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moshexx/airtable-backup",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.1.0",
        "colorama>=0.4.6",
        "emoji>=2.8.0",
        "schedule>=1.2.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "airtable-backup=src.backup:backup_airtable_to_csv",
            "airtable-backup-scheduler=src.schedule_backup:main",
        ],
    },
)