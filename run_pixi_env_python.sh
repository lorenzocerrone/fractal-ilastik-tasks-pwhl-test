
PACKAGE_ENV_DIR="/tmp/pixi_env"
MANIFEST_PATH="${PACKAGE_ENV_DIR}/pyproject.toml"
ENV_EXTRA="default" # Specify extra in pixi are installed in a separete env (dev, test, task-core)

# Run python in the pixi environment
pixi run --frozen --manifest-path $MANIFEST_PATH -e $ENV_EXTRA python -c "import ilastik_tasks; print(ilastik_tasks.__version__)"