#!/usr/bin/python3

import cgi
import cgitb
import subprocess
import re

# Enable detailed error messages for debugging
cgitb.enable()

def check_installation(package, package_manager):
    if package_manager == "yum":
        check_command = ["sudo", "yum", "list", "installed", package]
    elif package_manager == "pip":
        check_command = ["sudo", "pip", "show", package]
    else:
        return False, "Unsupported package manager."

    try:
        result = subprocess.run(check_command, capture_output=True, text=True, check=True)

        if package_manager == "yum":
            # Check if the package is in the output of 'yum list installed'
            if re.search(rf"\b{re.escape(package)}\b", result.stdout):
                return True, f"{package} is already installed."
            else:
                return False, f"{package} is not installed."
        elif package_manager == "pip":
            # Check if the package details are in the output of 'pip show'
            if re.search(rf"Name: {re.escape(package)}", result.stdout):
                return True, f"{package} is already installed."
            else:
                return False, f"{package} is not installed."
    except subprocess.CalledProcessError as e:
        return False, str(e)

def install_package(package, package_manager):
    if package_manager == "yum":
        install_command = ["sudo", "yum", "install", "-y", package]
    elif package_manager == "pip":
        install_command = ["sudo", "pip", "install", package]
    else:
        return False, "Unsupported package manager."

    try:
        process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read output and errors in real-time
        while process.poll() is None:
            output = process.stdout.readline().strip()
            if output:
                print(f"<p>{output}</p>")

        # Capture remaining output and errors
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return True, stdout
        else:
            return False, stderr
    except subprocess.CalledProcessError as e:
        return False, str(e)

def list_installed_packages(package_manager):
    if package_manager == "yum":
        list_command = ["sudo", "yum", "list", "installed"]
    elif package_manager == "pip":
        list_command = ["sudo", "pip", "list"]
    else:
        return "Unsupported package manager."

    try:
        result = subprocess.run(list_command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return str(e)

def main():
    form = cgi.FieldStorage()
    action = form.getvalue("action")
    package = form.getvalue("package")
    package_manager = form.getvalue("package_manager")

    print("Content-Type: text/html\n")

    if action == "install":
        if not package or not package_manager:
            print("<p>Error: Package or package manager not provided.</p>")
            return

        installed, message = check_installation(package, package_manager)
        if installed:
            print(f"<p>The package '{package}' is already installed.</p>")
        else:
            print(f"<p>Installing package '{package}'...</p>")
            success, output = install_package(package, package_manager)

            if success:
                print("<p>Package successfully installed.</p>")
            else:
                print("<p>Error installing package. Check logs for details.</p>")
                print("<pre>")
                print(output)
                print("</pre>")

    elif action == "list":
        if not package_manager:
            print("<p>Error: Package manager not provided.</p>")
            return

        installed_packages = list_installed_packages(package_manager)
        if installed_packages:
            print("<h2>Installed Packages:</h2>")
            print("<pre>")
            print(installed_packages)
            print("</pre>")
        else:
            print("<p>No packages found or an error occurred.</p>")

if __name__ == "__main__":
    main()
