# ipinfo

IPinfo Lite is a **free, unlimited, and accurate IP geolocation API & database** providing foundational country-level geolocation and ASN (Autonomous System Number) data with no usage caps and no credit card required.

It is designed for developers, startups, and enterprises that need reliable IP data for security, compliance, analytics, localization, and networking use cases.

---

## Overview

IPinfo Lite provides essential IP intelligence by mapping IP addresses to:

- Country & Continent
- ASN (Autonomous System Number)
- Organization name and domain

The data is updated daily and can be accessed via API or downloadable databases.

---

## Sample Request

You can test this process online at:

🔗 **[https://api.lukach.io/geo/ipinfo?134.129.111.111](https://api.lukach.io/geo/ipinfo?134.129.111.111)**

### Sample Output

```json
{
    "ip": "134.129.111.111",
    "geo": {
        "country": "United States",
        "country_code": "US",
        "continent": "North America",
        "continent_code": "NA"
    },
    "asn": {
        "id": "AS19530",
        "name": "State of North Dakota, ITD",
        "domain": "nd.gov"
    },
    "attribution": "IP address data powered by IPinfo, available from https://ipinfo.io.",
    "ipinfo_lite.mmdb": "Fri, 06 Feb 2026 11:00:01 GMT",
    "region": "us-east-1"
}
```

---

## Data Fields

| Field | Description |
|------|-------------|
| ip | Queried IP address |
| asn | Autonomous System Number |
| as_name | ASN organization name |
| as_domain | ASN organization domain |
| country_code | ISO 3166-1 alpha-2 country code |
| country | Country name |
| continent_code | Two-letter continent code |
| continent | Continent name |

---

## Common Use Cases

- Security monitoring and threat analysis
- Content localization
- Fraud detection and compliance
- Traffic analytics and reporting

---
