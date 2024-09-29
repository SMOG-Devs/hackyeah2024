from setuptools import find_packages, setup

setup(
    name='HackYeah',
    packages=find_packages(include=['whisper','video_processing','pathManager','transcription','VAD', 'OpenAINodes','metrics']),
    version='0.0.1',
    description='HackYeah',
    license='CC-BY-NC-ND',
)