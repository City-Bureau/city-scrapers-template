# City Scrapers Template

Template repo for running a [City Scrapers](https://cityscrapers.org) project in your area.

## Setup

- Fork this repo to your GitHub account or organization account. Feel free to change the name to something specific to your area (i.e. `city-scrapers-il` for scrapers in Illinois).
  - Enable issues for your fork by going to Settings, and checking the box next to Issues in the Features section.
- [Fill out this form](https://airtable.com/shrsdRcYVzp019U22) to join our [Slack channel](https://citybureau.slack.com/#labs_city_scrapers)
- Update `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `README.md` with your organization's information.
- Enable [Travis CI](https://travis-ci.org/) for running automated tests and builds.

  - Setup Azure or S3 for scraper output on your own account, or reach out to us for credentials for storage that we'll host.
  - Configure static file storage credentials as [environment variables in Travis CI](https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings). See [`city_scrapers/settings/prod.py`](./city_scrapers/settings/prod.py) to find out which environment variables need to be set for your storage provider.
  - Setup a daily cronjob on Travis CI ([see instructions](https://docs.travis-ci.com/user/cron-jobs/)) to run the scrapers.

- Setup a free open source account with [Sentry](https://sentry.io/for/open-source/) for error tracking and notifications. Set necessary environment variables and make sure `scrapy_sentry` is enabled in production settings.
- Refer to our documentation on [getting started with development](https://cityscrapers.org/docs/development/).
