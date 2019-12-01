# City Scrapers Template

Template repo for running a [City Scrapers](https://cityscrapers.org) project in your area.

## Setup

- [ ] Fork this repo or [create a new repo using it as a template](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template) in your GitHub account or organization account. Change the name to something specific to your area (i.e. `city-scrapers-il` for scrapers in Illinois).
  - If you forked the repo, enable issues for your fork by going to Settings, and checking the box next to Issues in the Features section.
- [ ] [Fill out this form](https://airtable.com/shrRv027NLgToRFd6) to join our [Slack channel](https://citybureau.slack.com/#labs_city_scrapers)
- [ ] Update `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `README.md` with your organization's information.
- [ ] Setup Azure or S3 for scraper output on your own account, or reach out to us for credentials for storage that we'll host.
- [ ] Setup a free open source account with [Sentry](https://sentry.io/for/open-source/) for error tracking and notifications.
- [ ] Configure credentials for static file storage and Sentry as [secrets in GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets). See [`city_scrapers/settings/prod.py`](./city_scrapers/settings/prod.py) to find out which environment variables need to be set for your storage provider.
- [ ] Uncomment the credentials for your storage provider and Sentry in the [`cron.yml` action](./.github/workflows/cron.yml).
- [ ] Uncomment the `on` sections of `ci.yml` and `cron.yml` to enable actions.
- [ ] Configure the time that scrapers should run daily in the [`cron.yml` action](./.github/workflows/cron.yml) (in UTC time).
- [ ] Refer to our documentation on [getting started with development](https://cityscrapers.org/docs/development/).
- [ ] Remove this checklist and replace with information for your project (feel free to refer to the main City Scrapers documentation site).
