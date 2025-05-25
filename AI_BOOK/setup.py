from setuptools import setup, find_packages

setup(
    name="aibook",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.2",
        "Jinja2>=3.1.6",
        "markdown>=3.7",
        "PyYAML>=6.0.1",
        "Werkzeug>=3.1.3",
        "cairosvg>=2.7.1"
    ],
    python_requires=">=3.8",
) 