# Developer answers: corrections

This file lists only corrections to statements the developer made himself. It leaves out:
- answers where he said "yes" to a claim that turned out wrong, because those are errors in our claims, not his;
- minor or overly specific details.

All paths are relative to `target/judo-ng-read/wt/`.

## K47: Per-class test runtime alone does not avoid the slow QueryFactory build

- **He wrote:** "the QueryFactory build is slow for testing, so we should build it at class level."
- **Correction:** `dataSourceMode = BY_CLASS` shares only the DataSource and the model loader. The Injector, `QueryFactory`, Liquibase executor and transaction manager are still rebuilt for **every test method**. To build them once per class you also need `shareInjector = true`; the Javadoc calls that combination the 5–10× speed-up.
- **Code:** `runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:171-189`

```java
@JudoTest(dataSourceMode = DataSourceMode.BY_CLASS, shareInjector = true)
```

Everything else he stated either matches the code or is about usage, which code cannot confirm (for example "measures are not in use" or "JCL is outdated").
