import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name="zerion-py",
  version="0.0.1",
  description="Zerion Software API Wrapper",
  long_description=README,
  long_description_content_type="text/markdown",
  url="https://github.com/jhsu98/zerion-py",
  author="Jonathan Hsu",
  author_email="jhsu98@gmail.com",
  license="MIT",
  packages=["zerionAPI"],
  python_requires='>=3.5',
  install_requires=[
      'pyjwt',
      'requests',
      'pytest'
  ],
  zip_safe=False
)