from setuptools import find_packages,setup

from typing import List

hypen_e_name ='-e .'

def get_requirements(file_path:str)->List[str]:

    """
    this is a function that returns a list of requirements
    """
    with open(file_path, 'r') as f:
        requirements=f.readlines()
        requirements=[requirement.replace('\n','') for requirement in requirements]
        if hypen_e_name in requirements:
            requirements.remove(hypen_e_name)
    return requirements
    
setup(
        name='mlproject',
        version='0.1.0',
        description='Machine Learning Project',
        author='Vivek Kumar',
        author_email='viv6267@gmail.com',
        packages=find_packages(), 
        install_requires=get_requirements('Requirements.txt'),  # here we are calling the function to get the requirements  
    )
