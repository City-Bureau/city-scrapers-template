import logging
import os

# https://jansonh.github.io/scrapinghub-gcs/
# If "GOOGLE_APPLICATION_CREDENTIALS" is the credential rather than a path,
# we need to write a local file with the credential.
path = "{}/google-cloud-storage-credentials.json".format(os.getcwd())

credentials_content = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

if not os.path.exists(credentials_content):
    with open(path, "w") as f:
        f.write(credentials_content)
    logging.warning("New path to credentials: %s" % path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
