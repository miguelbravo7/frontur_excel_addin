from setuptools import setup, find_namespace_packages

with open("README.md", 'r') as f:
    long_description = f.read()

with open("requirements.txt", 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="fronTur_excel_addin",
    author="Miguel Bravo Arvelo",
    author_email="alu0101031538@ull.edu.es",
    description="Trabajo de fin de grado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    packages=find_namespace_packages(),
    include_package_data=True,

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils'] + requirements,

    keywords="TFG ULL ISTAC",
    url="http://example.com/HelloWorld/",
    project_urls={
        "Documentation": "https://github.com/miguelbravo7/frontur_excel_addin#frontur_excel_addin",
        "Source Code": "https://github.com/miguelbravo7/frontur_excel_addin",
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        'Operating System :: Microsoft :: Windows',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3.7'
)
