setup(
    name="ton-minner",
    version="0.1.0",
    description="Minner",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Alex.hsieh",
    author_email="qwedsazxc78@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=[
        "numpy", "argparse", "requests", "pyopencl"
    ],
    entry_points={"console_scripts": ["ton-minner=:main"]},
)
