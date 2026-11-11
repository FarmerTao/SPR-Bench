# Security and evaluation isolation

Local validation runs trusted reference and deliberately defective project code.
It is not a sandbox for arbitrary submissions. The verifier's privilege dropping
is defense in depth, not a standalone security boundary.

Run untrusted agents and submissions only in disposable, isolated environments
without host credentials, host directory mounts or execution-time networking.
Test Harbor artifact transfer and separate verifier behavior before relying on
private-case isolation. The Docker integration has not yet been validated by
this release's authors.

All committed fixtures and reference solutions are public. Files called private
or hidden are hidden from an appropriately configured agent container, not from
repository readers. Do not use the public fixtures to claim uncontaminated blind
evaluation. See [evaluation guidance](docs/EVALUATION.md).

For a suspected sandbox escape or secret exposure, use GitHub's private
vulnerability reporting if enabled, or contact the maintainer through their
GitHub profile. Do not publish working escape details or secrets in public issues.
Scientific scoring errors without security impact can be reported normally.
