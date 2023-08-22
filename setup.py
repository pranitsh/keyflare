from setuptools import setup, find_packages

setup(
    name="KeyFlare",
    version="1.0.4",
    author="Pranit Shah",
    author_email="ppshah2023@gmail.com",
    description="Control your mouse with your keyboard through KeyFlare",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/Pshah2023/keyflare",
    install_requires=[
        "numpy==1.24.3",
        "opencv-python==4.7.0.72",
        "Pillow==9.5.0",
        "PyAutoGUI==0.9.54",
        "pynput==1.7.6",
        "pyperclip==1.8.2",
        "pyscreenshot==3.1",
        "Rtree==1.0.1"
    ],
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'keyflare=keyflare.__main__:main',
        ],
    },
)
