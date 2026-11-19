import json, re

SRC = "target/apply-findings/triage2/part-3.txt"
OUT_V = "target/apply-findings/triage/verdicts-r3.jsonl"
OUT_K = "target/apply-findings/triage/kept-r3.jsonl"

# keep: id -> (target, fact, already_documented)
KEEP = {
 "R1458": ("catalog/agent-docs/deployment/schema-evolution.md", "Incremental Liquibase diffs add a TableExists precondition to every table, because the previous-model check always returns true.", False),
 "R1459": ("catalog/agent-docs/deployment/schema-evolution.md", "The pre-check backup table name is the backup prefix, an underscore and the table SQL name, with no truncation or uppercasing.", False),
 "R1468": ("catalog/agent-docs/backend/type-system-guide.md", "REST enum attribute input literals are converted to the enum literal's integer value, not kept as literal strings.", False),
 "R1505": ("catalog/agent-docs/backend/platform-behavior-reference.md", "LocalDateTime is serialized in JSON with a UTC offset (ISO offset format, Z suffix), not without an offset.", True),
 "R1506": ("catalog/agent-docs/backend/authentication-guide.md", "Actor path matching is a raw string prefix match, so an actor path that is a prefix of another also matches its requests.", False),
 "R1559": ("catalog/agent-docs/model/ui-authoring-guide.md", "The JSL width modifier accepts any integer from 1 to 12, not only 1, 2, 3, 4, 6 and 12.", True),
 "R1560": ("catalog/agent-docs/model/jsl-language-notes.md", "The selector modifier accepts the literal keyword 'oldselector' alongside the selector keyword.", False),
 "R1567": ("catalog/agent-docs/deployment/schema-evolution.md", "The generated model-version is set to the project version, not to a timestamp, commit and branch composite.", False),
 "R1568": ("catalog/agent-docs/deployment/generator-plugins.md", "Entity tables are named T_ENTITIES_<NAME>.", True),
 "R1569": ("catalog/agent-docs/deployment/schema-evolution.md", "The schema module artifactId is <name><projectPostfix>-schema, and the Docker image name is the artifactId.", True),
 "R1581": ("catalog/agent-docs/deployment/application-config.md", "Generated projects ship a fixed placeholder identifier signer secret in judo-karaf.env, which must be replaced per environment.", False),
 "R1596": ("catalog/agent-docs/deployment/application-config.md", "A per-token upload MAX_FILE_SIZE applies only when it is larger than the server max size; smaller values are ignored.", False),
 "R1603": ("catalog/agent-docs/deployment/generator-plugins.md", "resetChecksums builds the checksum removers but never runs them, so it resets nothing.", False),
 "R1604": ("catalog/agent-docs/deployment/generator-plugins.md", "cleanGeneratedFromChecksum builds the checksum removers but never runs them, so it removes no generated files.", False),
 "R1605": ("catalog/agent-docs/deployment/generator-plugins.md", "synchronizeGitignore calls the checksum remover instead of the gitignore synchronizer, so the managed .gitignore block is not updated.", False),
 "R1607": ("catalog/agent-docs/deployment/generator-plugins.md", "A .gitignore START marker without an END marker drops every following line of the file.", False),
 "R1628": ("catalog/agent-docs/model/esm_metamodel/operation.md", "isMappedOperation treats an absent generateOperations flag as false, while shouldGenerateOperations treats it as true.", False),
 "R1632": ("catalog/agent-docs/backend/data-access-guide.md", "String aggregate expressions support only MIN and MAX; other operators, including concatenate, throw UnsupportedOperationException.", False),
 "R1664": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "The speed-dial toggle of a FAB group shows the group icon or no icon, never a SpeedDialIcon element.", False),
 "R1665": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "TextInput emits only maxLength; mask and regexp are not applied in the generated input.", False),
 "R1666": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "TextArea sets rows only; minRows is not emitted.", False),
 "R1667": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "A CharacterCounter renders only when countCharacters is set and the bound attribute has maxLength.", False),
 "R1668": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "There is no PasswordInput element type; password fields are not produced by a separate template.", False),
 "R1669": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "Numeric inputs use only the scale (decimalScale); precision has no effect.", False),
 "R1670": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "No Switch element is handled and no switch template exists; boolean inputs are not rendered as MUI Switch.", False),
 "R1671": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "baseUnit is not read; time inputs always show hours, minutes and seconds.", False),
 "R1672": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "EnumerationCombo renders an MUI Autocomplete, not a Select with MenuItem options.", False),
 "R1673": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "maxFileSize is not enforced client-side and binary uploads are not base64-encoded in the generated input.", False),
 "R1674": ("catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md", "Auto-focus goes to the first editable input that is not read-only, so a hidden input can receive focus.", False),
 "R1675": ("catalog/agent-docs/model/esm_metamodel/ui-visual-styleguide.md", "Child width is (12 / parent col) times child col in 12-column Grid units, not a percentage.", False),
 "R1676": ("catalog/agent-docs/model/esm_metamodel/ui-visual-styleguide.md", "A Flex renders a Card without elevation or radius props, and no isInCard flag propagates to children.", False),
 "R1677": ("catalog/agent-docs/model/esm_metamodel/ui-visual-styleguide.md", "A Flex gets the card branch from its card flag, not from having a frame.", False),
 "R1678": ("catalog/agent-docs/model/esm_metamodel/ui-visual-styleguide.md", "A Spacer renders a Grid with a fixed divider height and a width from col only; row is unused.", False),
 "R1679": ("catalog/agent-docs/frontend/i18n.md", "Translation files are written at public/i18n/application_default.json and public/i18n/application_<defaultLanguage>.json.", True),
 "R1680": ("catalog/agent-docs/frontend/i18n.md", "Translation keys are built from the root PageContainer name plus the element name, with no ClassType segment.", False),
 "R1682": ("catalog/agent-docs/frontend/i18n.md", "Enumeration keys use the restParamName of the enumeration type and add an enumerations.<type>._null key.", False),
 "R1683": ("catalog/agent-docs/frontend/i18n.md", "Menu keys use NavigationItem.getLabel(), not an item name.", False),
 "R1684": ("catalog/agent-docs/frontend/i18n.md", "i18next is initialised in l10n-context.tsx; src/config/general.ts holds toast and debounce settings, not i18n setup.", False),
 "R1685": ("catalog/agent-docs/frontend/build-and-deployment.md", "The frontend build script runs tsgo (TypeScript type-check) before vite build.", False),
 "R1689": ("catalog/agent-docs/backend/error-handling-guide.md", "ClientExceptionMapper falls back to HTTP 400 when the exception has no status code.", False),
 "R1690": ("catalog/agent-docs/backend/error-handling-guide.md", "RuntimeExceptionMapper passes ClientErrorException through, maps WebApplicationException to 400 or 500, and maps BusinessException to 422 with an X-Fault header.", True),
 "R1693": ("catalog/agent-docs/backend/error-handling-guide.md", "A WebApplicationException with a Jackson cause maps to 400 INVALID_JSON; null or RuntimeException causes map to 500; other checked causes map to 400.", False),
 "R1695": ("catalog/agent-docs/backend/error-handling-guide.md", "Client error bodies are exception.getDetails() as-is, with no code, message or details wrapper.", False),
 "R1696": ("catalog/agent-docs/backend/error-handling-guide.md", "PayloadMessageBodyWriter swallows every serialization error and leaves an empty entity.", False),
 "R1697": ("catalog/agent-docs/backend/debugging-and-monitoring-guide.md", "The X-Exchange-Id header is written only when an exchange id is set by ExchangeIdDecorator.", False),
 "R1699": ("catalog/agent-docs/backend/error-handling-guide.md", "Stack traces are embedded in error responses only when returnRuntimeExceptions is true.", False),
 "R1702": ("catalog/agent-docs/backend/platform-behavior-reference.md", "JSON responses are written with the platform default charset, not UTF-8.", False),
 "R1704": ("catalog/agent-docs/backend/type-system-guide.md", "The DATE_FORMAT key is never read, so the ISO 8601 date parameter format cannot be configured through it.", False),
 "R1706": ("catalog/agent-docs/backend/authentication-guide.md", "An access point without @actor counts as public, and one public access point makes the whole operation public.", False),
 "R1726": ("catalog/agent-docs/deployment/build-process.md", "import_postgres sorts the dump list through a pipeline assignment that changes nothing, so dumps are not sorted before import.", False),
 "R1747": ("catalog/agent-docs/model/model-validation-and-transformation.md", "The Esm2Ui transformation defaults to ETL in code, while the Javadoc says ZETA is the default.", False),
 "R1800": ("catalog/agent-docs/deployment/spring-boot-runtime.md", "Only hsqldb and postgresql dialect bundles ship; this checkout has no Oracle dialect bundle.", True),
 "R1822": ("catalog/agent-docs/model/jsl-language-notes.md", "A member with required set to false is still treated as required, because isRequired checks only that the modifier is present.", False),
 "R1896": ("catalog/agent-docs/e2e-testing/README.md", "The generated e2e aggregate pom's build section contains only pluginManagement and omits the extra-plugins fragment.", False),
 "R1898": ("catalog/agent-docs/deployment/application-config.md", "The Guice Keycloak integration reads its settings from JudoKeycloakModuleConfiguration, not from KEYCLOAK_* environment variables.", False),
 "R1899": ("catalog/agent-docs/deployment/application-config.md", "The Keycloak server URL default in JudoKeycloakModuleConfiguration is http://localhost:8080/auth, and the connector default differs.", False),
 "R1900": ("catalog/agent-docs/deployment/application-config.md", "The Keycloak admin password default is 'judo' in JudoKeycloakModuleConfiguration and 'admin' in KeycloakConnectorProvider.", False),
 "R1901": ("catalog/agent-docs/backend/authentication-guide.md", "KeycloakLoginInterceptor verifies the token without an explicit issuer-to-realm check.", False),
 "R1971": ("catalog/agent-docs/backend/data-access-guide.md", "The static query navigation QueryCustomizer name is <impl package>.<name>QueryCustomizerImpl, which does not match the emitted class.", False),
 "R2006": ("catalog/agent-docs/backend/custom-operations.md", "The operation input parameter map key uses the raw input name, while the method signature uses the lowerFirst name.", False),
 "R2030": ("catalog/agent-docs/deployment/build-process.md", "judo.sh accepts -f and --build-frontend-module for frontend builds; the misspelled --build-fronted-module is not accepted.", True),
 "R2031": ("catalog/agent-docs/deployment/build-process.md", "The start command accepts only -w and --skip-watch-bundles; the documented -W flag is not parsed.", False),
 "R2032": ("catalog/agent-docs/deployment/build-process.md", "The java_compiler start option is documented but judo.sh never reads it.", False),
 "R2033": ("catalog/agent-docs/deployment/build-process.md", "A standalone ignore-checksum token is ignored; checksum skipping is set per command with -i.", True),
 "R2036": ("catalog/agent-docs/deployment/build-process.md", "install_maven_wrapper is defined but never called, so maven-wrapper.properties keeps the judo-ng Nexus URL.", False),
 "R2037": ("catalog/agent-docs/deployment/build-process.md", "The start example's -o option has an unbalanced double quote, so the documented command does not parse.", True),
 "R2041": ("catalog/agent-docs/deployment/local-development.md", "The application HTTP port defaults to 8181 (Karaf HTTP), not 8080; 8080 is the Keycloak default.", True),
 "R2043": ("catalog/agent-docs/deployment/production.md", "The health endpoint is /system/health?tags=<model>&format=json; no /health route is generated.", True),
 "R2044": ("catalog/agent-docs/deployment/application-config.md", "Database settings use JUDO_PLATFORM_RDBMS_DB_* variables (HOST, DATABASE, USER, PASSWORD).", True),
 "R2046": ("catalog/agent-docs/deployment/application-config.md", "The filestore directory is set by JUDO_PLATFORM_FILESTORE_DIRECTORY; JUDO_PLATFORM_FILESTORE_PATH is not read.", False),
 "R2048": ("catalog/agent-docs/deployment/application-config.md", "The Keycloak server URL variable is JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL; KEYCLOAK_URL is not read.", True),
 "R2049": ("catalog/agent-docs/backend/testing-guide.md", "Generated poms define no integration-tests profile; the profiles are build-model, build-schema and similar.", False),
 "R2089": ("catalog/agent-docs/deployment/generator-plugins.md", "The systemVariables parameter of the JSL generator Maven plugin reads environment variables instead of system properties.", False),
}

# duplicate: id -> of_id
DUP = {
 "R1644": "R1632", "R1692": "R1690", "R1694": "R1693", "R1701": "R1696",
 "R1707": "R1693", "R1748": "R1747", "R2035": "R1726", "R2042": "R2041",
 "R2045": "R2044", "R2047": "R2044",
}

# not-platform reasons by repo / kind for everything else
def np_reason(repo, kind, rid):
    if repo == ".":
        return "judo-ng repo docs, CI or contributor tooling"
    if repo.startswith("community-documentation") or repo.startswith("documentation"):
        return "docs site content, not platform behaviour"
    if repo.startswith("eclipse/"):
        return "Eclipse or EMF plumbing, not app-facing"
    if repo.startswith("packages/"):
        return "OSGi packaging metadata, not app-facing"
    if repo.startswith("tools/"):
        return "build tooling internals, not app-facing"
    if kind == "dox":
        return "module agent-doc for framework internals"
    if repo.startswith("template/"):
        return "template or UI generator defect, not documented behaviour"
    return "framework internals, not app-facing"

lines = [l.rstrip("\n") for l in open(SRC, encoding="utf-8") if l.strip()]
ids = []
verdicts = []
kept = []
for l in lines:
    parts = l.split(" | ", 4)
    rid, kind, repo, pathline = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
    ids.append(rid)
    ev_path = re.sub(r"@[0-9a-f]+(?=:)", "", pathline)
    ev_repo = "judo-ng" if repo == "." else repo
    evidence = f"{ev_repo}:{ev_path}"
    if rid in KEEP:
        target, fact, already = KEEP[rid]
        verdicts.append({"id": rid, "verdict": "keep", "reason": "app-facing platform behaviour"})
        kept.append({"id": rid, "target": target, "fact": fact, "evidence": evidence, "already_documented": already})
    elif rid in DUP:
        verdicts.append({"id": rid, "verdict": "duplicate", "reason": f"same fact as {DUP[rid]}"})
    else:
        verdicts.append({"id": rid, "verdict": "not-platform", "reason": np_reason(repo, kind, rid)})

assert len(ids) == len(set(ids)), "duplicate input ids"
missing_keep = set(KEEP) - set(ids)
missing_dup = set(DUP) - set(ids)
assert not missing_keep and not missing_dup, (missing_keep, missing_dup)
for d in DUP.values():
    assert d in KEEP, d

with open(OUT_V, "w", encoding="utf-8") as f:
    for v in verdicts:
        f.write(json.dumps(v, ensure_ascii=False) + "\n")
with open(OUT_K, "w", encoding="utf-8") as f:
    for k in kept:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")

from collections import Counter
c = Counter(v["verdict"] for v in verdicts)
already = sum(1 for k in kept if k["already_documented"])
print("input", len(ids))
print("verdict lines", len(verdicts), "unique ids", len({v["id"] for v in verdicts}))
print(dict(c))
print("kept", len(kept), "already_documented", already)
