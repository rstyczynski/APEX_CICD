# Native SQLcl PROJECT version compatibility

Observed on 2026-11-03 using a temporary clone of the application repository,
the existing native lab-dev-c connection and author schema E1_DEV_C.

The project records `sqlcl.version = 25.4.1.0`. SQLcl build 26.3.0.260.1620
rejected `project export -list` with:

```text
SQLcl Version Mismatch expected 25.4.1.0 found 26.3.0.0
```

It suggested updating project configuration, but no such update was made.
This invocation returned process status zero; callers must inspect operation
results and cannot infer success from exit status alone.

With SQLcl build 25.4.1.022.0618, the existing capture SQL listed 21 objects and
exported 22 objects, including APEX application 810003. The profile's identity
query returned E1_DEV_C. A deliberately nonexistent profile supplied at client
startup (`-L -name`) returned status one and did not execute the supplied SQL.
These checks performed no deployment or database password reset.

Oracle's [PROJECT command reference](https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.3/sqcug/project.html)
documents inspecting and changing `sqlcl.version` through native project config.
The mismatch above is an observed native release constraint. The project's
same-qualified-build policy and production acceptance requirements are recorded
in [NFR-5](../../../docs/srs.md#quality-requirements-and-initial-release).
Full upgrade qualification and all production gates are not claimed by this
bounded export check.

The corrected workstation discovery was executed from the application checkout.
It checked the installed 26.3, 25.3 and 25.4 clients, selected the release
recorded by project metadata, and reported build 25.4.1.022.0618 in 7.0 seconds
on the prepared host. Searches were restricted to tool locations, excluding
dependency/Git directories. Each version probe used `-nohistory -noupdates`,
closed standard input and a visible path diagnostic. This avoids sharing the
loop's file-list input with SQLcl; cancellation is not reported as proof that
an installation is absent.
