# City Scrapers Template

[![CI build status](https://github.com/City-Bureau/city-scrapers-template/workflows/CI/badge.svg)](https://github.com/City-Bureau/city-scrapers-template/actions?query=workflow%3ACI)
[![Cron build status](https://github.com/City-Bureau/city-scrapers-template/workflows/Cron/badge.svg)](https://github.com/City-Bureau/city-scrapers-template/actions?query=workflow%3ACron)

Template repo for creating a [City Scrapers](https://cityscrapers.org/) project in your area to scrape, standardize and share public meetings from local government websites. You can find more information on the [project homepage](https://cityscrapers.org/) or in the original City Scrapers repo for the Chicago area: [City-Bureau/city-scrapers](https://github.com/City-Bureau/city-scrapers).

## Setup

In order to set up a City Scrapers project for your area you'll need a GitHub account as well as git, Python 3.6 or above and [Pipenv](https://pipenv.pypa.io/en/latest/) installed. If you want to make it easy to share access and onboard new contributors, [GitHub organizations](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams) are a free and easy way of doing that.

1. Create a new repo in your GitHub account or organization by [using this repo as a template](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) or forking it.

   - You should change the name to something specific to your area (i.e. `city-scrapers-il` for scrapers in Illinois)
   - If you forked the repo, enable issues for your fork by going to Settings, and checking the box next to Issues in the Features section.

2. Clone the repo you created (substituting your account and repo name) with:

   ```shell
   git clone https://github.com/{ACCOUNT}/city-scrapers-{AREA}.git
   ```

3. Update `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `README.md` with info on your group or organization so that people know what your project is and how they can contribute.

4. Create a Python 3.8 virtual environment and install development dependencies with:

   ```shell
   pipenv install --dev --python 3.8
   ```

   If you want to use a version other than 3.8 (3.6 and above are supported), you can change the version for the `--python` flag.

5. Decide whether you want to output static files to AWS S3, Microsoft Azure Blob Storage, or Google Cloud Storage, and update the `city-scrapers-core` package with the necessary extras:

   ```shell
   # To use AWS S3
   pipenv install 'city-scrapers-core[aws]'
   # To use Microsoft Azure
   pipenv install 'city-scrapers-core[azure]'
   # To use Google Cloud Storage
   pipenv install 'city-scrapers-core[gcs]'
   ```

   Once you've updated `city-scrapers-core`, you'll need to update [`./city_scrapers/settings/prod.py`](./city_scrapers/settings/prod.py) by uncommenting the extension and storages related to your platform.

   **Note:** You can reach out to us at [documenters@citybureau.org](mailto:documenters@citybureau.org) or on our [Slack](https://airtable.com/shrRv027NLgToRFd6) if you want free hosting on either S3 or Azure and we'll create a bucket/container and share credentials with you. Otherwise you can use your own credentials.

6. Create a free account on [Sentry](https://sentry.io/), and make sure to [apply for a sponsored open source account](https://sentry.io/for/open-source/) to take advantage of additional features.

7. The project template uses [GitHub Actions](https://docs.github.com/en/actions) for testing and running scrapers. All of the workflows are stored in the `./.github/workflows` directory. You'll need to make sure Actions are [enabled for your repository](https://docs.github.com/en/github/administering-a-repository/disabling-or-limiting-github-actions-for-a-repository).

   - [`./.github/workflows/ci.yml`](./.github/workflows/ci.yml) runs automated tests and style checks on every commit and PR.
   - [`./.github/workflows/cron.yml`](./.github/workflows/cron.yml) runs all scrapers daily and writes the output to S3, Azure, or GCS. You can set the `cron` expression to when you want your scrapers to run (in UTC, not your local timezone).
   - [`./.github/workflows/archive.yml`](./.github/workflows/archive.yml) runs all scrapers daily and submits all scraped URLs to the Internet Archive's [Wayback Machine](https://archive.org/web/). This is run separately to avoid slowing down general scraper runs, but adds to a valuable public archive of website information.
   - Once you've made sure your workflows are configured, you can change the URLs for the status badges at the top of your `README.md` file so that they display and link to the status of the most recent workflow runs. If you don't change the workflow names, all you should need to change is the account and repo names in the URLs.

8. In order for the scraped results to access S3, Azure, or GCS as well as report errors to Sentry, you'll need to set [encrypted secrets](https://docs.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets) for your actions. Set all of the secrets for your storage backend as well as `SENTRY_DSN` for both of them, and then uncomment the values you've set in the `env` section of `cron.yml`. If the `cron.yml` workflow is enabled, it will now be able to access these values as environment variables.

9. Once you've set the storage backend and configured GitHub Actions you're ready to write some scrapers! Check out our [development docs](https://cityscrapers.org/docs/development/) to get started.

10. We're encouraging people to contribute to issues on repos marked with the [`city-scrapers`](https://github.com/topics/city-scrapers) topic, so be sure to set that on your repo and add labels like "good first issue" and "help wanted" so people know where they can get started.

11. If you want an easy way of sharing your scraper results, check out our [`city-scrapers-events`](https://github.com/City-Bureau/city-scrapers-events) template repo for a site that will display the meetings you've scraped for free on [GitHub Pages](https://pages.github.com/).

## Next Steps

There's a lot involved in starting a City Scrapers project beyond the code itself, so you can check out our [Introduction to City Scrapers](https://cityscrapers.org/docs/introduction/) in our documentation for some notes on how to grow your project.

If you want to ask questions or just talk to others working on City Scrapers projects you can [fill out this form](https://airtable.com/shrRv027NLgToRFd6) to join our Slack channel or reach out directly at [documenters@citybureau.org](mailto:documenters@citybureau.org).
