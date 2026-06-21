from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="data-viz-portfolio",
    version="1.0.0",
    description="Production-quality data visualizations built with Matplotlib & Seaborn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jai Krishna",
    author_email="your@email.com",
    url="https://github.com/<your-username>/data-viz-portfolio",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "plotly>=5.18.0",
        "scipy>=1.11.0",
        "scikit-learn>=1.3.0",
        "flask>=3.0.0",
        "Pillow>=10.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "flake8>=7.0.0",
            "isort>=5.13.0",
            "jupyter>=1.0.0",
            "ipykernel>=6.26.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "dataviz-build=build_all:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords="data visualization matplotlib seaborn charts dashboard portfolio",
    project_urls={
        "Bug Reports": "https://github.com/<your-username>/data-viz-portfolio/issues",
        "Source":      "https://github.com/<your-username>/data-viz-portfolio",
    },
)
