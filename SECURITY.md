# Security and data boundaries

The shipped web interface is a loopback-only, single-user research service. It deliberately binds to `127.0.0.1`; the CLI exposes no option to bind all interfaces. Do not place this server behind a public reverse proxy. Python's `http.server` documentation states that it is not recommended for production [PYTHON-HTTP]. The implementation adds an exact asset allowlist, Host and Origin checks, a custom local request header, request-size limits, finite numeric checks, closed experiment names and bounded simulation work. These are defensive constraints, not a penetration-test certificate.

There is no authentication, multi-tenant isolation, TLS termination, institutional access control, clinical device interface, remote execution, cloud upload, telemetry, external script or model API dependency. The UI does not persist inputs. CLI commands write only to the explicitly chosen output directory; a nonempty run directory is not overwritten. Files remain in that directory until the operator deletes them. Local users and administrators can read those files subject to operating-system permissions.

Use synthetic and appropriately authorized research data only. The server does not need patient data and has no field for patient identity. Free text in an evidence file can still contain sensitive information; no automatic de-identification is claimed. The `evidence` CLI validates declarations, not privacy compliance.

HTML output escapes dynamic strings. CSV text beginning with spreadsheet formula prefixes is prefixed with an apostrophe; numeric negative values remain numeric. Receipt paths reject traversal and symlinks. The local server neither lists directories nor serves arbitrary working files. Long-running experiments are capped; the server remains a simple single-process teaching service and is not resilient to malicious local denial of service.

A hash chain is not a signature. Rewriting the complete ledger and receipt can create another internally consistent bundle. Preserve the printed receipt digest in an independent trusted channel to detect that class of replacement. Nothing in the receipt proves an external source true or a human authorized a medical action.

Report problems privately to the eventual repository maintainers. This package does not invent a security email address or promise a response time. The GitHub CI file is provided as configuration; local test results do not imply the hosted workflow has run.
