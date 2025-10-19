# EtilbudsavisHomeAssistance
An intergration of etilbudsavis to home assistance.

## Installing integration on home assistant
To add the integration to your home assistant, follow these steps:

1. **Go to HACS (Home Assistant Community Store):**
Go to HACS -> Integrations -> Custom repositories -> Add repository.

2. **Add url:**
Add this url: https://github.com/soeren97/EtilbudsavisHomeAssistance.

3. **Select category:**
Select integration as category.

4. **Add integration:**
Click "Add".

5. **Restart**
Restart your home assistant and the integration should now be under integrations.

## Etilbudsavis API key & secret
To use this integration an API key and secret is needed these can be obtained here: https://tjek.com/apis-and-sdks

## Development
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

### Additional Notes:
- **Virtual Environment:** Creating a virtual environment is a good practice to isolate project dependencies from other projects and the system Python environment.
- **pip Install:** The `pip install .` command installs the necessary packages specified in the `setup.py` file from the current directory.
- **requirements** The required packages can be found in the `setup.py` file as the variable `INSTALL_REQQUIRES`.