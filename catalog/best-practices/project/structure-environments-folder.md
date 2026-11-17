---
id: structure-environments-folder
title: Environments Folder and Root Runtime Config Files
description: "Keep local runtime selection in the root properties files, and every deployed target (test, demo, prod) in its own environments/<env>/ folder with infrastructure code, operator scripts, a compose shape and git-ignored secrets."
aliases: [deployment environments folder, per-environment config, enviroments, environment layout, compose properties]
keywords: [environments, prod, test, demo, terraform, manage.sh, compose-dev.properties, compose-full.properties, judo-karaf.env, env example, tfvars, secrets, gitignore]
tags: ["domain:project", "layer:backend", "project:rackinspect", "project:park-here", "project:mlszksz-platform", "status:emerging"]
category: structure
status: emerging
projects: [rackinspect, park-here, mlszksz-platform]
evidence: ["rackinspect:enviroments/", "rackinspect:compose-dev.properties", "park-here:src/environments/", "park-here:src/judo-karaf.env.example", "mlszksz-platform:enviroments/"]
alternatives: []
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

A JUDO project runs in two kinds of places: on a developer machine (local Karaf or a local Compose stack) and on deployed targets (test, demo, prod). Keep the two apart: local runtime selection in a few root files, deployed targets in one folder per environment, and no secret in git in either.

## Practice

### Platform base: the root runtime files

- `judo.properties` is the default set of start options; the build script's environment option selects an alternate properties file instead, such as `compose-dev.properties` with `runtime=compose` and `compose_env=compose-develop` ([selecting an environment](../../agent-docs/deployment/application-config.md#selecting-an-environment-judosh-env)).
- The template ships two Compose profiles under `application/docker/` (`compose-develop` and `compose-postgresql-https`) ([shipped Compose environments](../../agent-docs/deployment/production.md#shipped-docker-compose-environments)). The observed projects keep one root selector file per profile: `compose-dev.properties` and `compose-full.properties`.
- `judo-karaf.env` holds the `JUDO_PLATFORM_*` variables. The template does not generate per-environment env files ([selecting an environment](../../agent-docs/deployment/application-config.md#selecting-an-environment-judosh-env)), and real credentials must stay out of version control ([security best practices](../../agent-docs/deployment/application-config.md#security-best-practices)).

### Practice notes: the root secret file

- Put `judo-karaf.env` in `.gitignore` and commit a `judo-karaf.env.example` with placeholder values. Also keep it in `.generator-ignore`, see [[generator-ignore-config-protection]].
- Do not commit a filled `judo-karaf.env`: a root file that holds the signer secret, the SMTP password and an admin password must stay out of git.

### Practice notes: one folder per deployed target

```
environments/
  AGENTS.md or README.md     # operator guide, differences between targets
  test/  demo/  prod/
    manage.sh                # operator entry point (deploy, start, stop, status)
    terraform/               # infrastructure as code for this target
    app-compose/             # compose shape of the application host
    images/                  # staged image tars (ignored)
    .env                     # target values and secrets (ignored)
```

- One subfolder per target with the same structure, so a diff between `test/` and `prod/` shows the real differences.
- Ignore the value files (`environments/*/.env`, `*.auto.tfvars`); commit only templates or examples.
- Document intended differences between targets in the folder's `AGENTS.md` or README, so nobody "syncs" them by accident.
- If the deployed compose file is rendered from an infrastructure template, mark the committed compose file as a shape reference and test that it matches.
- Add guard scripts at the folder root: one check confirms that test and prod do not reuse the same secret value, and another validates the tfvars files.
- Wire init-time admin users and the identifier signer secret through every target ([provisioning a new environment](../../agent-docs/deployment/application-config.md#provisioning-a-new-environment-prod--test--demo)).
- Name the folder `environments`. A misspelt copy, `enviroments`, carries the typo into every script path.

## Rationale

- Developers keep using the platform's local workflow without touching deployment files.
- Each deployed target is reproducible from its own folder, and secrets never enter git.
- Cost: the per-target folders duplicate scripts; changes must be ported between targets on purpose.

## Example

- One project: `environments/test/` and `environments/prod/` with `manage.sh`, `terraform/`, `app-compose/` and runbooks; `check-env-collisions.sh` and `validate-tfvars.sh` at the folder root; root `judo-karaf.env` ignored and an example committed.
- Another project: `environments/demo|test|prod/` with the same structure, an `AGENTS.md` that states prod differs on purpose and that its compose file is shape-only; root `compose-dev.properties` and `compose-full.properties`.
- A third project: `environments/dev|test|prod/` with a `README.md` and an operator cheat sheet; root `judo-karaf.env` ignored.

## When to avoid

- A project deployed only by a separate platform team or a central GitOps repository keeps the per-target configuration there; keep only the root runtime files in the application repository.

## Related

- [[structure-repository-root-layout]] — the rest of the root layout
- [[generator-ignore-config-protection]] — protecting `judo.properties` and `judo-karaf.env` from regeneration
- [[osgi-karaf-bundle-architecture]] — the runtime these files configure
