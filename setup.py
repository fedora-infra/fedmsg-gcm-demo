from setuptools import setup

setup(
    name='gcmconsumer',
    version='1.0.0',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=["fedmsg"],
    packages=[],
    entry_points="""
    [moksha.consumer]
    gcmconsumer = gcmconsumer:GCMConsumer
    """,
)
