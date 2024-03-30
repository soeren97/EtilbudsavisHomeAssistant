# EtilbudsavisHomeAssistance
An intergration of etilbudsavis to home assistance.

## Installation Guide

### Prerequisites:
- Anaconda installed
- pip installed (usually comes with Anaconda)

### Steps:

1. **Clone the Repository:**
`git clone https://github.com/soeren97/EtilbudsavisHomeAssistance`

2. **Navigate to the Repository Directory:**
`cd */EtilbudsavisHomeAssistance`

3. **Create a Virtual Environment (Optional but Recommended):**
`conda create -n your-env-name python=3.11`

4. **Activate the Virtual Environment:**
`conda activate your-env-name`

5. **Install Required Packages:**
`pip install .`

6. **Verify Installation:**
Ensure all dependencies are installed successfully without any errors.

7. **Deactivate Virtual Environment (If Created):**
`conda deactivate`

8. **Create config.json.**
Create a file containing the fields key and secret in the repocetory directory, with the two being api key and secret.


### Additional Notes:

- **Virtual Environment:** Creating a virtual environment is a good practice to isolate project dependencies from other projects and the system Python environment.
- **pip Install:** The `pip install .` command installs the necessary packages specified in the `setup.py` file from the current directory.
- **requirements** The required packages can be found in the `setup.py` file as the variable `INSTALL_REQQUIRES`.