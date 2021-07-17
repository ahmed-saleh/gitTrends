from setuptools import setup

setup(
    name="gitTrends",
    version="0.1",
    py_modules=["trends"],
    include_package_data=True,
    install_requires=["click", "pygit2", "pytz", "react"],
    entry_points="""
        [console_scripts]
        trends=trends:cli
    """,
)