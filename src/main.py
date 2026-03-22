import os
import subprocess

def generate_docs():
    """Automatically generate documentation for the project."""
    # Use Sphinx to generate HTML documentation
    subprocess.run(['sphinx-build', '-b', 'html', 'docs', 'docs/_build/html'])
    print("Documentation generated successfully!")

if __name__ == "__main__":
    generate_docs()