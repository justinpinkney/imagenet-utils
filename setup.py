from setuptools import setup

setup(
        name="imagenet_utils",
        version="0.1",
        entry_points="""
        [console_scripts]
        imagenet-utils=imagenet_utils.cli:cli
        """,
        )
