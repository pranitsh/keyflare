"""Setup.py for pip installation"""
import pathlib
from setuptools import setup, find_packages

def main():
    """Performs the setup"""
    setup(
        name="keyflare",
        version="1.1.3",
        author="Pranit Shah",
        author_email="ppshah2023@gmail.com",
        description="Control your mouse with your keyboard through KeyFlare",
        long_description=pathlib.Path("README.md").read_text(encoding="utf8"),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=["tests*", "test_*", "*tests*"]),
        url="https://github.com/Pshah2023/keyflare",
        install_requires=[
            "numpy==1.24.3",
            "opencv-python==4.7.0.72",
            "Pillow==9.5.0",
            "PyAutoGUI==0.9.54",
            "pynput==1.7.6",
            "pyperclip==1.8.2",
            "pyscreenshot==3.1",
            "Rtree==1.0.1",
            "numpy==1.24.3"
        ],
        extras_require={
            "dev": [
                "pytesseract==0.3.1",
                "twine==4.0.2",
                "wheel==0.41.3",
                "pytest==7.4.2",
                "pytest-benchmark==4.0.0",
                "setuptools==68.2.2",
            ]
        },
        license="MIT",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
        ],
        entry_points={
            "console_scripts": [
                "keyflare=keyflare.__main__:main",
            ],
        },
    )


if __name__ == "__main__":
    main()
