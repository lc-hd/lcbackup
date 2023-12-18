# This is an example of the environment variables of interest
# Dockerfile will source env-local.sh

# ----for dev of prod environments
DEBUG_VALUE=

# --------------for connecting to db
export DB_NAME=
export DB_USER=
export DB_PASS=
export DB_HOST=
export DB_PORT=
# --------------for connecting to db

# -------------------------------------for connecting to s3 bucket
export DBBACKUP_ACCESS_KEY=
export DBBACKUP_BUCKET_NAME=
export DBBACKUP_ENDPOINT_URL=
export DBBACKUP_SECRET_KEY=
# -------------------------------------for connecting to s3 bucket
