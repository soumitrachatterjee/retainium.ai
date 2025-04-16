from setuptools import setup, find_packages

setup(
    name="retainium.ai",
    version="0.1.0",
    author="Soumitra Chatterjee",
    description="A CLI-based Knowledge Management System with embedding and LLM support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/soumitrachatterjee/retainium.ai",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "chromadb>=0.4.21",
        "langchain>=0.1.0",
        "sentence-transformers>=2.2.2",
        "nltk>=3.8.1",
        "tqdm>=4.66.1",
        "configparser>=5.3.0",
        "uuid",  # comes with stdlib in Python 3, can be omitted if needed
    ],
    entry_points={
        "console_scripts": [
            "retainium=retainium.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    license="AGPL-3.0",
)
