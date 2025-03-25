from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'  # Corrected typo from HYPEN to HYPHEN

def get_requirements(file_path: str) -> List[str]:
    '''
    This function returns a list of requirements from the given file.
    
    Args:
        file_path (str): Path to the requirements file (e.g., 'requirements.txt')
    Returns:
        List[str]: List of package requirements
    '''
    requirements = []
    try:
        with open(file_path, 'r') as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.strip() for req in requirements]  # Remove newlines and whitespace
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. No requirements will be installed.")
    return requirements

setup(
    name='ReviewAnalyzer',
    version='0.0.1',
    author='Aniska',
    author_email='nayakaniska918@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)