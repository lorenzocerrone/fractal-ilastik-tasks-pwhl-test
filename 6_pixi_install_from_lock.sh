PACKAGE_ENV_DIR="/tmp/pixi_env"
MANIFEST_PATH="${PACKAGE_ENV_DIR}/pyproject.toml"
ENV_EXTRA="dev" # Specify extra in pixi are installed in a separete env (dev, test, task-core)

# Create the environment using pixi
pixi install --manifest-path $MANIFEST_PATH -e $ENV_EXTRA --frozen