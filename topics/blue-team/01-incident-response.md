---
title: Incident Response
subtitle: What to do, in what order, when something goes wrong
course: Blue Team
---

# The Basics
Incidents will happen. A plan decides whether they become disasters.

## Event, alert, incident
- **Event**: anything observable that happens on a system: a login, a file write
- **Alert**: an event a tool flagged as possibly bad
- **Incident**: a confirmed violation of security policy that needs a response
- **Breach**: an incident where data was actually accessed or stolen

## The NIST incident response lifecycle
1. **Preparation**: plans, tools, training, contacts
2. **Detection & analysis**: spot it, confirm it, scope it
3. **Containment, eradication & recovery**: stop it, remove it, restore
4. **Post-incident activity**: lessons learned, improve
> The lifecycle is a loop: lessons from step 4 feed back into preparation.
Note: NIST SP 800-61 is the reference. SANS uses six steps (PICERL) that cover the same ground.

# Preparation & Detection

## Preparation
- An **IR plan** with roles: incident lead, analysts, comms, legal
- **Playbooks** for common cases: phishing, ransomware, lost laptop
- Logging in place **before** you need it: endpoints, servers, network, cloud
- A contact list, out-of-band communication, and a jump bag of tools

## Detection sources
| Source | Example signal |
|---|---|
| SIEM alert | 50 failed logins then a success |
| EDR | Office spawning PowerShell |
| Network / IDS | Beaconing to a rare domain every 60 s |
| User report | "I clicked a link and entered my password" |
| Third party | A partner or the police tells you |

## Analysis: the questions to answer
- **What** happened, and is it really malicious?
- **When** did it start? Build a timeline
- **Where**: which hosts, accounts and data are affected?
- **How** did they get in, and are they still here?
- **Severity**: what is the business impact?

## Triage example: a suspicious login
```text
2026-03-14 02:13:07  4625  Failed logon   user=j.doe   src=185.220.101.4
2026-03-14 02:13:09  4625  Failed logon   user=j.doe   src=185.220.101.4
2026-03-14 02:13:15  4624  Logon (type 10) user=j.doe  src=185.220.101.4
2026-03-14 02:14:02  4688  New process    powershell.exe -enc JABjAGwA...
# Failed logons, then RDP success from a foreign IP at 2am, then encoded PowerShell
```
- Remote logon at an unusual hour from an unknown IP
- Followed by **encoded PowerShell**
- Treat as an **incident**: escalate

# Containment to Recovery

## Containment
- **Short term**: isolate the host from the network, block the IP, disable the account
- **Long term**: rebuild trust: patch, reset credentials, add monitoring
- **Preserve evidence** before wiping anything: memory, disk image, logs
> Pulling the power destroys memory evidence. Isolate the network instead.

## Evidence handling
1. Collect the most **volatile** data first: memory, then disk
2. **Hash** every image so you can prove it never changed
3. Keep a **chain of custody**: who had it, when, and why
4. Analyse **copies**, never the original

## Eradication & recovery
- Remove malware, persistence and attacker accounts
- Close the entry point: patch, fix the misconfiguration
- Restore from **known-good** backups
- Watch closely afterwards: attackers often try to come back

## Lessons learned
- Hold a **blameless** review within two weeks
- What happened, what worked, what didn't
- Turn findings into actions: new detections, playbook changes, training
- Track metrics: **time to detect**, **time to contain**

## ? A ransomware alert fires on one laptop. What do you do first?
- **Isolate** the laptop from the network to stop the spread
- Don't power it off: memory may hold the encryption key and evidence
- Check for the same activity on other hosts, then follow the ransomware playbook

## Key takeaways
- Prepare before the incident: plans, logs, contacts
- Analyse: what, when, where, how, how bad
- Contain without destroying evidence
- Every incident should improve your defences
