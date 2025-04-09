from setuptools import setup, find_packages

setup(
    name="text_translation",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "pydantic[email]",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "transformers",
        "torch"
    ],
)
