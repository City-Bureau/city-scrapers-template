# Scenarios

Many government websites share similar technology stacks, and we've built out some common approaches to a few of these.

## Legistar

Legistar is a software platform provided by Granicus that many governments use to hold their legislative information. If you run into a site using Legistar (typically you'll know because `legistar.com` will be in the URL), then you should use the `legistar` package to run the scraper and avoid unnecessary work. You can refer to spiders like `alle_county` or `pitt_city_council` to see examples of this approach.

## ASP.NET Sites

ASP.NET sites can be a challenge because they're often inconsistent and require maintaining a level of state across requests. You can see an example of handling this behavior in the [`cuya_administrative_rules`](https://github.com/City-Bureau/city-scrapers-cle/blob/master/city_scrapers/spiders/cuya_administrative_rules.py) spider.
