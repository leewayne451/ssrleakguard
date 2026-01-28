from setuptools import setup, find_packages

setup(
    name="ssrleakguard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "ssrleakguard=ssrleakguard.cli:main",
        ],
    },
    author="Your Name",
    description="Security testing tool for SSR web applications",
    python_requires=">=3.8",
)