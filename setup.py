from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-url-group-permissions",  # Replace with your package name
    version="1.0",  # Initial version
    author="Elazos",  # Your name or organization
    author_email="info@elazos.com",  # Your email
    description="A Django package for managing URL-based permissions through user groups with HTTP method support",
    long_description=long_description,  # Long description from README
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/jmarxuach/django-url-group-permissions",  # Project URL
    project_urls={
        "Bug Tracker": "https://github.com/jmarxuach/django-url-group-permissions/issues",  # Issue tracker
    },
    classifiers=[
        "Development Status :: 3 - Alpha",  # Package maturity
        "Framework :: Django",
        "Framework :: Django :: 3.2",  # Django version compatibility
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",  # License
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
    ],
    packages=find_packages(),  # Automatically find packages in the directory
    include_package_data=True,  # Include non-Python files (e.g., templates, static files)
    python_requires=">=3.7",  # Python version requirement
    install_requires=[
        "Django>=3.2",  # Django dependency
    ],
    extras_require={
        "dev": [
            "black",  # Code formatting
            "flake8",  # Linting
            "pytest",  # Testing
            "pytest-django",  # Django testing
        ],
    },
)