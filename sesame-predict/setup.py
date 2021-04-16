import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sesame-predict",
    author="Writwick Das",
    author_email="writwick.das@rwth-aachen.de",
    description="cli predictor for Open Sesame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['open-sesame']
)