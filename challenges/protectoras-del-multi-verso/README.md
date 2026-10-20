# Protectoras del Multi-Verso — TheM4rv3ls CTF

**Category:** Web Hacking · **Points:** 130 · **Environment:** WordPress CTF lab

**Focus:** HTTP request analysis, authentication flow, administrative file-editing risk, remote command execution, filesystem enumeration, Base64 decoding.

> **Documentation note:** I completed this CTF challenge, but I did not retain a complete original evidence set. This retrospective reconstruction documents the attack path and recovered flag. The historical WordPress environment was **not re-accessed** for this write-up, and screenshots/recordings created by other people are not presented as my own evidence.

## Challenge objective

The fictional Carol Danvers runs a WordPress website hiding information about her activities. The task is to obtain access to the challenge environment, locate the protected material, and extract a flag.

This exercise follows [Más allá de lo visible](../mas-alla-de-lo-visible/README.md), which yielded candidate credentials for the fictional **CarolDanvers** account through OSINT and cryptographic decoding. Those CTF-specific credentials supplied the intended pivot into the WordPress challenge.

**Scope:** An intentionally configured competition instance. The workflow below describes a historical CTF solution, not authorization to test any present-day public server.

## Investigation at a glance

| Phase | Observation | Outcome |
| --- | --- | --- |
| 1. Web reconnaissance | The website presented as a WordPress installation | Authentication identified as an entry point |
| 2. Request inspection | The visible login flow sent a password parameter but omitted the username | Inconsistent form submission isolated |
| 3. Authentication | A locally constructed login form supplied both expected fields | Authenticated administrative WordPress session |
| 4. Privileged site access | Administrative plugin management was available | Ability to work with WordPress files |
| 5. Code execution in the lab | Server-executed PHP was placed in an editable application file | Reverse connection and shell access described in the original solve |
| 6. Filesystem exploration | A directory named `/opt/S.H.I.E.L.D./` was located | Lead toward secret material |
| 7. Flag extraction | A saved Base64 payload decoded to a flag | Challenge result recovered and checked offline |

## 1. Inspect the WordPress site

The challenge page led to a dedicated website branded **Protectoras del Multi-Verso**, featuring a themed homepage and a WordPress login/admin area.

Trying to sign in through the provided interface resulted in a blocking browser alert:

```text
NUNCA PODRÁS ACCEDER
```

Rather than assuming the credentials were wrong, I investigated **how the form submitted them**.

## 2. Inspect the login request with Burp Suite

Using **Burp Suite Community Edition** and its HTTP history, the captured login request showed an unexpected parameter pattern (target address omitted):

```http
GET /wp-login.php?pwd=<redacted>&wp-submit=Acceder&redirect_to=<redacted>&testcookie=1 HTTP/1.1
Host: <historical-ctf-target>
```

**Key finding:** the request contained a `pwd` query parameter but did **not** contain WordPress's expected `log` username parameter. The password also appeared in the URL rather than in a POST body, an avoidable exposure risk when handling real credentials.

This observation supports the hypothesis that the provided interface or its submission behavior had been altered. It does **not**, on its own, prove a vulnerability in WordPress core.

The distinction matters: **the form and the server-side authentication handler are separate components**. A broken or modified user interface does not necessarily mean the underlying authentication endpoint is disabled.

## 3. Correct the expected authentication flow

The earlier CTF puzzle supplied the fictional account name `CarolDanvers` and a candidate password. A locally prepared HTML form was used to send the normal WordPress field names to the expected endpoint:

| Form parameter | Purpose |
| --- | --- |
| `log` | Username |
| `pwd` | Password |
| HTTP `POST` | Submits the credentials in the request body instead of the URL query string |

The recorded outcome was a successful **authenticated WordPress administrative session**.

**Important:** This was a CTF credential-and-form-flow exercise, not authentication bypass without credentials. The password is omitted here; its derivation is described in the earlier challenge write-up.

## 4. Understand the administrator-to-code-execution boundary

Once logged in, the WordPress administrative interface exposed plugin-management capabilities. The historical solve used a file-management plugin, **Advanced File Manager**, to access and edit files in the WordPress installation.

The relevant security lesson is not that installing this named plugin always constitutes a vulnerability. It is that **an account with administrative rights plus permission to modify server-executed PHP can potentially turn CMS access into operating-system-level code execution**.

Within the scoped CTF environment, the documented sequence was:

1. Install and activate a file-management plugin from the administrative dashboard.
2. Prepare a PHP connection payload for the controlled lab.
3. Use the plugin's editor to change an accessible PHP file (shown as `index1.php` in the recorded sequence).
4. Arrange an outbound connection to a controlled listener; a TCP forwarding service was used because the local machine was behind NAT.
5. Request the PHP file, resulting in a reverse shell in the historical challenge.

No deployable PHP shell, active callback address, or third-party target URL is included in this repository. The controlled session was used only to investigate the competition instance.

### What this demonstrated

The important escalation was:

```CTF credentials
    → authenticated WordPress administration
    → write access to executable PHP
    → server-side command execution
    → filesystem investigation
```

The level of operating-system privilege obtained through PHP was not separately documented. A reverse shell does **not** imply root access.

## 5. Investigate the challenge filesystem

The recorded shell session navigated to `/opt` and discovered a directory spelled **`S.H.I.E.L.D.`** (including its final dot).

```text
/opt/
└── S.H.I.E.L.D./
    └── Danvers/
```

This naming is useful context: the investigator initially attempted to enter `S.H.I.E.L.D` without the final period, which failed; using the complete directory name worked.

The notes also describe a secret text file named **`ExpedienteSecreto.txt`** containing an encoded value. However, that file was **not visible in the later remote directory listing**. The available record shows the payload preserved in a local file with that name, so this write-up does not claim to freshly retrieve it from the server or independently verify its final remote location.

## 6. Decode the recovered Base64 string

The recorded text was:

```text
bXJtYXJ2ZWx7M2JlZTE5MTc5NDg4Mzk3NzBmZDEzNDZmODcyZmUwZjJ9
```

This is standard Base64 encoding. Using **CyberChef → From Base64** or a local standard-library decoder produces:

```text
mrmarvel{3bee1917948839770fd1346f872fe0f2}
```

**Recovered CTF flag:** `mrmarvel{3bee1917948839770fd1346f872fe0f2}`

The Base64 string and decoded result were independently checked offline while preparing this document. That verification confirms the transformation, but it does **not** verify the historical shell session or current availability of the competition host.

To reproduce this specific transformation, run the included Python helper:

```bash
python3 challenges/protectoras-del-multi-verso/scripts/decode_flag.py
```

## Security implications and remediation

| Observed behavior | Security significance | Defensive measure |
| --- | --- | --- |
| Password sent as a URL query parameter | Credential exposure in browser history, logs, and related telemetry | Use HTTPS with correctly configured POST-based authentication |
| Modified or malfunctioning login page | Authentication UI cannot be assumed to reflect server behavior | Validate form behavior and server-side authentication controls |
| Administrative plugin installation | High-privilege users can extend CMS functionality | Enforce least privilege, MFA, and controlled plugin approval |
| Editable server-executable PHP | CMS file write can cross into code execution | Restrict write permissions, disable unnecessary file editors, monitor integrity |
| Outbound shell connection from a web server | Possible unauthorized control and exfiltration channel | Restrict egress, monitor web-server child processes and outbound connections |

## Lessons learned

1. **Inspect requests before assuming credentials failed.** Burp made the missing username parameter obvious.
2. **Do not confuse client-side friction with server-side enforcement.** A blocking alert is not an access-control boundary.
3. **Understand the privilege chain.** Administrator access became important because it enabled modification of server-executable application code.
4. **Look closely at exact filesystem names.** Here, the final period in `S.H.I.E.L.D.` mattered.
5. **Validate what can actually be reproduced.** The recorded Base64 payload was independently decoded; the original WordPress compromise was not rerun for this documentation.
6. **Separate a CTF demonstration from a general product claim.** The write-up does not assert that a normal, securely configured WordPress site is vulnerable in the same way.

## Tools and technologies

**WordPress · Burp Suite · Kali Linux · Advanced File Manager · PHP · TCP forwarding/NAT · Linux shell · CyberChef · Python 3**

*Educational documentation of a historical, intentionally scoped CTF environment only. No live target access was performed when compiling this write-up.*
