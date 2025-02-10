
PACKAGE_ENV_DIR="./pwhl_env"
PWHL_PATH="./dist/ilastik_tasks-0.1.dev26+gd6b1ff9.pwhl.zip"
MANIFEST_PATH="${PACKAGE_ENV_DIR}/pyproject.toml"
ENV_EXTRA="dev" # Specify extra in pixi are installed in a separete env (dev, test, task-core)

# Unzip the pwhl file
unzip $PWHL_PATH -d $PACKAGE_ENV_DIR

# Create the environment using pixi
pixi install --manifest-path $MANIFEST_PATH -e $ENV_EXTRA