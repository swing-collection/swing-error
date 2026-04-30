# Changelog

## Unreleased

- reorganized pytest coverage under `tst/cases` with per-module mirrored tests
- split multi-symbol internals into single-symbol implementation files behind stable facades
- added default security headers to error responses
- added `Retry-After` auto-detection support for `Http429Response`
- scrubbed sensitive request data from error logging
- added async `__acall__` support to `ExceptionMiddleware`
- fixed package metadata typo and curated the top-level public API
