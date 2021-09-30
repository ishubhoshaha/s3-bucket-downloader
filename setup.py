from setuptools import setup
from s3_bucket_downloader import __version__

extra_dev = [
]

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name = 's3-bucket-downloader',
    version = __version__,
    description = "AWS S3 Bucket Downloader",
    long_description=readme,

    url = 'https://github.com/ishubhoshaha/s3-bucket-downloader',
    author = 'Shubho Shaha',
    author_email = 'ishubhoshaha@gmail.com',
    install_requires = ['boto3', 'botocore', 'alive-progress'],
    py_modules = ['s3_bucket_downloader'],
    keywords = ['python', 'devops-tools', 'aws'],
    classifiers= [
            "Development Status :: 1 - Alpha",
            "Intended Audience :: DevOps",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X"
        ]
)