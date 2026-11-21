---
title: Reconnaissance & OSINT
subtitle: Learning about a target before touching it
course: Red Team
---

# Before You Start
Recon is the first phase of every engagement, and the one that decides how the rest goes.

## Rules of engagement come first
- Only test systems you have **written authorisation** for
- The **scope** lists exactly which domains, IP ranges and people are in bounds
- Agree on **timing**, allowed techniques and an emergency contact
- Out of scope means out of scope, even if it looks vulnerable
> No signed scope, no testing. Unauthorised scanning is illegal in most countries.
Note: Spend time here when teaching. Students should be able to explain what a scope document contains.

## Where recon fits
1. **Reconnaissance**: gather information
2. **Scanning & enumeration**: map live hosts and services
3. **Exploitation**: gain initial access
4. **Post-exploitation**: escalate, move, persist
5. **Reporting**: explain findings and fixes

## Passive vs active recon
| | Passive | Active |
|---|---|---|
| Touches the target? | No | Yes |
| Detectable by target | Very unlikely | Possible: logs, IDS |
| Examples | Search engines, DNS records, certificates | Port scans, banner grabbing |
| Needs authorisation | Still within scope rules | Always |

# OSINT Sources
Open-source intelligence: information anyone can legally find.

## What you are looking for
- **Domains & subdomains**: every web-facing system the organisation runs
- **IP ranges**: who owns which address blocks
- **People**: names, roles and email formats, for phishing assessments
- **Technology**: web servers, frameworks, cloud providers, VPN products
- **Leaks**: exposed documents, code repositories, old credentials

## DNS and WHOIS
- `whois` shows who registered a domain and who owns an IP block
- DNS records reveal mail servers, name servers and services
- Zone transfers (AXFR) sometimes leak the whole zone if misconfigured
```bash
whois example.com
dig example.com ANY +noall +answer
dig example.com MX +short
dig example.com TXT +short        # SPF, verification records
dig axfr @ns1.example.com example.com
```

## Finding subdomains
- **Certificate Transparency** logs list every TLS certificate issued for a domain
- Search engines with operators: `site:example.com -www`
- Passive DNS datasets and tools like **amass** and **subfinder**
```bash
# certificates issued for the domain (crt.sh)
curl -s "https://crt.sh/?q=%25.example.com&output=json" | jq -r '.[].name_value' | sort -u
subfinder -d example.com -silent
amass enum -passive -d example.com
```

## Search engine dorking
| Query | Finds |
|---|---|
| site:example.com filetype:pdf | Public documents and their metadata |
| site:example.com inurl:login | Login portals |
| site:github.com "example.com" | Code mentioning the company |
| intitle:"index of" site:example.com | Open directory listings |

## People and email formats
- Company site, LinkedIn and press releases give names and roles
- Work out the email pattern: `first.last@`, `flast@`
- Tools like **theHarvester** collect emails and hosts from public sources
- Use this only for **in-scope** social engineering tests
> Treat personal data you collect carefully: store it securely and delete it after the engagement.

# Turning Data Into a Plan

## Organise what you find
- **Asset list**: domains, IPs, owners, what each one runs
- **Attack surface**: which assets are exposed and how
- **Priorities**: old software, admin panels, forgotten subdomains first
- **Evidence**: note the source and time of every finding

## Defender's view
- Search for yourself: run the same recon on your own organisation
- Remove old DNS records and forgotten subdomains
- Strip metadata from public documents
- Watch Certificate Transparency for certificates you didn't request

## ? Is reading a company's certificate transparency logs passive or active recon?
- **Passive**: you query a public log, not the company's servers
- The target never sees your traffic
- It is still covered by the engagement's scope and rules

## Key takeaways
- Authorisation and scope come before everything
- Passive first, active only when in scope
- DNS, certificates and search engines reveal a lot
- Organise findings into an attack surface map
