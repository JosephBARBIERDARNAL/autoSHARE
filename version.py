

import subprocess
packages = ['pandas', 'streamlit']
requirements_file = 'requirements.txt'



def getPackageVersion(package_name: str) -> str:
    """
    Get the version of a package using pip show.
    Args:
        package_name: Name of the package to get the version for.
    Returns:
        The version of the package.
    """

    try:
        result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True)
        details = result.stdout.split('\n')
        for line in details:
            if line.startswith('Version: '):
                return line.split(' ')[1]
    except Exception as e:
        print(f"Error getting version for package {package_name}: {str(e)}")
    return None


with open(requirements_file, 'w') as file:
    for package in packages:
        version = getPackageVersion(package)
        if version:
            packageVersion = f"{package}=={version}"
            print(packageVersion)
            file.write(packageVersion+'\n')
        else:
            print(f"Version not found for package {package}")

print("\nRequirements file updated")
