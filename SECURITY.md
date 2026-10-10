# Security policy

## Reporting a vulnerability

Please report security problems privately through GitHub's **"Report a vulnerability"**
button on the repository's Security tab (private vulnerability reporting). Do not open a
public issue for a vulnerability.

Include what you found, how to reproduce it, and what an attacker could do with it. You
should get an acknowledgement within 7 days. Fixes are released as a new version with a
CHANGELOG entry, and reporters are credited unless they ask not to be.

## Supported versions

Security fixes go into the latest release only.

## What is in scope

- The approval gate: anything that lets an unapproved rule execute, or lets a decision be
  recorded against an identity that did not make it.
- The review log: anything that alters or removes a recorded decision without
  `verify_chain` reporting it. Note the documented limit: the chain is unkeyed and lives in
  the same database, so a database administrator can rewrite it.
- The reviewer application and the calculation API: authentication, CSRF, injection,
  disclosure of household data.
- The extraction pass: prompt-injection text in a source reaching an approved rule without
  being escalated.

## Design rules that reports are judged against

- Household data is never stored by the calculation API, and never sent to a language model.
- A missing fact evaluates to unknown, never to a default.
- Nothing a model proposes executes without a recorded human approval.
