import json, os, re

BASE = "/Users/bmiller/Projects/judo-blueprint"
IN = os.path.join(BASE, "target/apply-findings/triage2/part-4.txt")
OUT_V = os.path.join(BASE, "target/apply-findings/triage/verdicts-r4.jsonl")
OUT_K = os.path.join(BASE, "target/apply-findings/triage/kept-r4.jsonl")

lines = [l.rstrip("\n") for l in open(IN, encoding="utf-8") if l.strip()]
rows = []
for l in lines:
    parts = [p.strip() for p in l.split(" | ")]
    rows.append({"id": parts[0], "kind": parts[1], "repo": parts[2], "path": parts[3]})

# keep: id -> (target, fact, evidence, already_documented, reason)
KEEP = {
 "R2116": ("frontend/../backend/platform-behavior-reference.md",
   "Empty-string rejection for required string attributes runs only when the validator option is ACCEPT_NON_EMPTY; no option is applied by default.",
   "judo-runtime-core:judo-runtime-core-validator/src/main/java/hu/blackbelt/judo/runtime/core/validator/DefaultPayloadValidator.java:367", False,
   "Required-string empty check has no default; doc claims ACCEPT_NON_EMPTY default"),
 "R2117": ("backend/patterns-and-best-practices.md",
   "The validation context has no rootPayload key; it holds the global validation context plus location and related keys.",
   "judo-runtime-core:judo-runtime-core-validator/src/main/java/hu/blackbelt/judo/runtime/core/validator/DefaultPayloadValidator.java:169", False,
   "Custom validators cannot read a rootPayload context key"),
 "R2123": ("backend/error-handling-guide.md",
   "With ignoreInvalidValues set, attribute validation is skipped, including the required-attribute check.",
   "judo-runtime-core:judo-runtime-core-validator/src/main/java/hu/blackbelt/judo/runtime/core/validator/DefaultPayloadValidator.java:203", False,
   "ignoreInvalidValues also skips required checks"),
 "R2202": ("frontend/esm-to-ui-mappings/widgets.md",
   "A FAB button group with one button and featuredActions=0 renders nothing, because SpeedDial needs more than one button.",
   "judo-ui-react-template:judo-ui-react/src/main/resources/actor/src/containers/widget-fragments/fab-button-group.fragment.hbs:5", False,
   "Single-button FAB group renders nothing"),
 "R2203": ("frontend/esm-to-ui-mappings/widgets.md",
   "hiddenBy is applied to featured FAB buttons but not to SpeedDial items in a FAB group.",
   "judo-ui-react-template:judo-ui-react/src/main/resources/actor/src/containers/widget-fragments/fab-button-group.fragment.hbs:22", False,
   "hiddenBy ignored for SpeedDial FAB items"),
 "R2204": ("frontend/esm-to-ui-mappings/widgets.md",
   "Dialog FAB groups render after DialogContent and are positioned fixed, not inside the dialog body.",
   "judo-ui-react-template:judo-ui-react/src/main/resources/actor/src/containers/dialog.tsx.hbs:173", False,
   "Dialog FAB placement differs from documented overlay"),
 "R2215": ("deployment/application-config.md",
   "poolSize is stored in the Guice PostgreSQL module configuration but is never applied to the HikariCP pool.",
   "judo-runtime-core:judo-runtime-core-guice-postgresql/src/main/java/hu/blackbelt/judo/runtime/core/guice/dao/rdbms/postgresql/PostgresqlDataSourceProvider.java:70", False,
   "poolSize setting has no effect on pool"),
 "R2279": ("model/jcl-operation-scripts.md",
   "String '>' comparison in a script generates Java with a stray character, so the generated code does not compile.",
   "judo-script-codegen:generator/src/main/java/hu/blackbelt/judo/script/codegen/generator/Script2JavaGenerator.xtend:1025", False,
   "Script string '>' generates invalid Java"),
 "R2280": ("model/jcl-operation-scripts.md",
   "String '<=' comparison in a script generates Java with a stray character, so the generated code does not compile.",
   "judo-script-codegen:generator/src/main/java/hu/blackbelt/judo/script/codegen/generator/Script2JavaGenerator.xtend:1027", False,
   "Script string '<=' generates invalid Java"),
 "R2281": ("model/jcl-operation-scripts.md",
   "A for-all expression in a script is generated as an exists check.",
   "judo-script-codegen:generator/src/main/java/hu/blackbelt/judo/script/codegen/generator/Script2JavaGenerator.xtend:942", False,
   "For-all script expression generated as exists"),
 "R2293": ("e2e-testing/troubleshooting.md",
   "The generated playwright.config.ts sets retries to 4 for every run, not only on CI.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/playwright.config.ts.hbs:15", True,
   "Generated Playwright retries apply on every run"),
 "R2294": ("e2e-testing/helpers-reference.md",
   "clearPrimitiveField accepts a backCheck argument that is never used, so no value check runs after clearing.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/utils.ts.hbs:154", False,
   "clearPrimitiveField backCheck parameter has no effect"),
 "R2295": ("e2e-testing/helpers-reference.md",
   "createSingleRelationElement does not await submitSingleRelationElementCreate, so the submit promise is unhandled.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/utils.ts.hbs:235", False,
   "Generated single-relation helper misses await"),
 "R2296": ("e2e-testing/helpers-reference.md",
   "createCollectionRelationElement does not await submitCollectioRelationElementCreate, so the submit promise is unhandled.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/utils.ts.hbs:317", False,
   "Generated collection helper misses await"),
 "R2297": ("e2e-testing/helpers-reference.md",
   "acceptChangesOnDialogElement clicks an Ok button with a different icon label than the other Ok helpers.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/utils.ts.hbs:331", False,
   "Dialog accept helper uses different Ok label"),
 "R2298": ("e2e-testing/helpers-reference.md",
   "Labels in generated Playwright locators are escaped only for double quotes; backslashes and newlines are emitted raw.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/java/hu/blackbelt/judo/ui/generator/playwright/VisualElementHelper.java:204", False,
   "Generated locator labels not fully escaped"),
 "R2299": ("e2e-testing/model-screen-layout.md",
   "Container, table and tab elements without children are generated as leaves, without their _id/_label (and tab) entries.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/java/hu/blackbelt/judo/ui/generator/playwright/VisualElementHelper.java:281", False,
   "Childless containers emitted as leaves"),
 "R2301": ("e2e-testing/helpers-reference.md",
   "APP_URL is interpolated into a RegExp without escaping, so regex metacharacters in the URL change what is matched.",
   "judo-ui-e2e-template:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/ApiHelper.ts.hbs:4", False,
   "APP_URL used unescaped in RegExp"),
 "R2324": ("backend/platform-behavior-reference.md",
   "A ListCall that joins an existing transaction is not rolled back; the rollback happens only when the call started a new transaction.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/AlwaysRollbackTransactionalBehaviourCall.java:69", False,
   "Read rollback applies only to new transactions"),
 "R2348": ("backend/authentication-guide.md",
   "AuthenticationInterceptor.success runs before the CRUD authorizers, so it can fire for an operation that later fails with PERMISSION_DENIED.",
   "judo-runtime-core:judo-runtime-core-accessmanager/src/main/java/hu/blackbelt/judo/runtime/core/accessmanager/DefaultAccessManager.java:145", False,
   "Doc says success follows access checks; code differs"),
 "R2418": ("deployment/application-config.md",
   "dispatcherMetricsReturned defaults to false in the Guice default module configuration.",
   "judo-runtime-core:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/JudoDefaultModule.java:92", False,
   "dispatcherMetricsReturned default is false"),
 "R2456": ("frontend/hooks/action-hooks.md",
   "Container hooks refresh data through context.actions.refresh(); context.refresh() is not the documented API.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/data-hooks.md.hbs:271", False,
   "Refresh API name conflicts between hook docs"),
 "R2457": ("frontend/hooks/action-hooks.md",
   "lodash debounce returns the result of the last completed call, so the first awaited call can yield undefined.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/action-hooks.md.hbs:263", True,
   "Debounced autocomplete returns stale or undefined results"),
 "R2517": ("frontend/error-handling.md",
   "The generated FeedbackLevel type includes 'WARNING ' with a trailing space.",
   "judo-ui-typescript-rest-template:judo-ui-typescript-rest-api/src/main/resources/common/errors/FeedbackLevel.ts.hbs:1", False,
   "Generated FeedbackLevel literal has trailing space"),
 "R2533": ("frontend/i18n.md",
   "application_*.json translation files are generated and regenerated, so they are not safe to edit.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:578", True,
   "Generated translation files are regenerated, not editable"),
 "R2534": ("frontend/i18n.md",
   "JUDO translation keys are flat dot-notation strings, not nested objects.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/i18n.md.hbs:256", True,
   "Translation keys are flat dot-notation"),
 "R2535": ("frontend/hooks/validation-hooks.md",
   "Async validation results are read as result.data?.exists, so the response shape is { data: { exists } }.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/validation-hooks.md.hbs:690", True,
   "Async validation example destructures wrong shape"),
 "R2536": ("frontend/hooks/ui-hooks.md",
   "APPBAR_COMPONENTS_INTERFACE_KEY is not defined or imported by the generated template set.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:609", False,
   "AppBar interface key used but never defined"),
 "R2537": ("frontend/model-screen-layout.md",
   "Generated text fields use translation keys of the form entities.<Entity>.<Component>.<field>.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/model-screen-layout.md.hbs:242", True,
   "Generated field translation key convention"),
 "R2541": ("frontend/hooks/ui-hooks.md",
   "Menu customization must copy menuItems before sorting, because sort() mutates the array the framework passes.",
   "judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/frontend/hooks/ui-hooks.md.hbs:478", True,
   "Framework menu array is mutated by sort"),
 "R2481": ("frontend/advanced-patterns.md",
   "The generated relation remove<Rel> posts the unserialized selected objects instead of the serialized input array.",
   "judo-ui-typescript-rest-template:judo-ui-typescript-rest-axios/src/main/resources/data-axios/relationServiceImpl.ts.hbs:309", False,
   "Generated relation remove posts unserialized payload"),
 "R2469": ("backend/data-access-guide.md",
   "Setter names for embedded mapped relations are built with a double dot (relation..name) in the collection branch.",
   "judo-psm-generator-sdk-core:judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dto.for.create.builder.java.hbs:60", False,
   "Embedded relation builder setter name malformed"),
 "R2494": ("deployment/tooling-guide.md",
   "The schema merge relation re-sync guard never matches, because the merge descriptor feature is not a schema RelationFeature.",
   "judo-esm-schema-merge-maven-plugin:src/main/resources/script/merge.eol:211", False,
   "Schema merge relation re-sync guard never matches"),
 "R2495": ("deployment/tooling-guide.md",
   "The schema merge throws 'Super type not defined in target' when the supertype is in the target, the reverse of its condition.",
   "judo-esm-schema-merge-maven-plugin:src/main/resources/script/merge.eol:125", False,
   "Schema merge supertype check is inverted"),
 "R2563": ("model/judo-cli.md",
   "The judo.sh dumps list is not sorted: the sort pipeline result is discarded because the pipeline starts with an assignment.",
   "judo-tatami-tests:generator-template/src/main/resources/models/model/judo.sh.hbs:332", False,
   "judo.sh dumps list is not sorted"),
 "R2618": ("backend/platform-behavior-reference.md",
   "With no IdentifierSignerSecret bound, identifiers are still signed with a random per-process HMAC key; there is no unsigned mode.",
   "judo-runtime-core:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/dispatcher/AGENTS.md:9", False,
   "Unbound signer secret does not mean unsigned identifiers"),
 "R2620": ("deployment/application-config.md",
   "rdbmsDaoMarkSelectedRangeItems is never bound in the module, so setting it has no effect.",
   "judo-runtime-core:judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/JudoDefaultModuleConfiguration.java:56", False,
   "Config option rdbmsDaoMarkSelectedRangeItems has no effect"),
 "R2719": ("backend/platform-behavior-reference.md",
   "The optimistic-lock VERSION check runs only when the update payload contains __version.",
   "judo-runtime-core:judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:144", True,
   "Optimistic lock check condition on __version presence"),
 "R2741": ("backend/data-access-guide.md",
   "Generated count() with query parameters references an undeclared effectiveParams variable, so the generated code does not compile.",
   "judo-psm-generator-sdk-core:judo-psm-generator-sdk-core-impl/src/main/resources/dao/impl/querycustomizer.implementation.java.hbs:117", False,
   "Generated count() with parameters fails to compile"),
 "R2828": ("deployment/build-process.md",
   "scanDependencies is initialised to false in code while its Maven @Parameter default is true.",
   "judo-spring-maven-plugin:judo-spring-maven-plugin/src/main/java/hu/blackbelt/judo/spring/maven/plugin/TransformerWorkflowMojo.java:98", False,
   "scanDependencies default differs between code and parameter"),
 "R2831": ("backend/interceptors.md",
   "The default interceptor provider does not read a Guice Multibinder set; it returns an empty list unless interceptors are configured explicitly.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/create-interceptor/SKILL.md:136", False,
   "Guice Multibinder registration does not add interceptors"),
 "R2832": ("backend/interceptors.md",
   "A Spring @Bean returning OperationCallInterceptor is not collected; the Spring configuration returns an empty interceptor list.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/create-interceptor/SKILL.md:158", False,
   "Spring @Bean interceptor registration does not run"),
 "R2833": ("backend/error-handling-guide.md",
   "No OperationNotFoundException class exists; a missing operation surfaces as an InternalServerException.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/debug-operations/SKILL.md:90", False,
   "OperationNotFoundException does not exist"),
 "R2834": ("backend/error-handling-guide.md",
   "ValidationException has no getViolations() method; it is built from a collection of ValidationResult.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/debug-operations/SKILL.md:124", False,
   "ValidationException getViolations does not exist"),
 "R2837": ("integration-testing/getting-started.md",
   "No alwaysRollback test setting exists; AlwaysRollbackTransactionalBehaviourCall is only a base class.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/debug-operations/SKILL.md:188", False,
   "alwaysRollback test setting does not exist"),
 "R2838": ("backend/platform-behavior-reference.md",
   "EnvironmentVariableProvider is a concrete class implementing Function<String, Object> with apply(String), not an interface with get().",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/dispatcher-architecture/SKILL.md:173", False,
   "EnvironmentVariableProvider is a class with apply"),
 "R2839": ("backend/platform-behavior-reference.md",
   "DispatcherFunctionProvider exposes getSdkFunctions() and getScriptFunctions(), each returning Map<EOperation, Function<Payload, Payload>>.",
   "judo-runtime-core:judo-runtime-core-dispatcher/src/main/resources/claude/plugins/judo-dispatcher/skills/dispatcher-architecture/SKILL.md:189", False,
   "DispatcherFunctionProvider method names differ"),
 "R2847": ("integration-testing/getting-started.md",
   "The @JudoTest modelName annotation default is \"example\".",
   "judo-runtime-core:judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:44", False,
   "@JudoTest default modelName is example"),
 "R2848": ("integration-testing/getting-started.md",
   "resolveDialect is package-private, so application test code cannot call it.",
   "judo-runtime-core:judo-runtime-core-guice-testkit/agent-docs/api-reference.md:24", False,
   "resolveDialect is not public"),
 "R2849": ("integration-testing/getting-started.md",
   "tearDown rolls back an open transaction only; it does not close the injector or datasource.",
   "judo-runtime-core:judo-runtime-core-guice-testkit/agent-docs/api-reference.md:17", False,
   "tearDown does not close injector or datasource"),
 "R2850": ("integration-testing/getting-started.md",
   "The testkit does not read injection annotations; it injects all eligible fields and set* setters.",
   "judo-runtime-core:judo-runtime-core-guice-testkit/agent-docs/api-reference.md:154", False,
   "Testkit injection is not annotation driven"),
 "R2851": ("integration-testing/getting-started.md",
   "Derived test artifacts are reused across methods only when shareInjector is true; the default false rebuilds them.",
   "judo-runtime-core:judo-runtime-core-guice-testkit/TEST-CONFIGURATION.md:300", False,
   "Artifact caching only with shareInjector"),
}

DUP = {
 "R2217": "R2215", "R2760": "R2279", "R2761": "R2280", "R2762": "R2281",
 "R2772": "R2299", "R2540": "R2457", "R2499": "R2494", "R2470": "R2469",
 "R2624": "R2620", "R2347": "R2348", "R2350": "R2348",
}

# Explicit not-platform reasons for specific ids
NP_OVERRIDE = {
 "R2118": "Claim matches VALIDATOR location code (uses '/' between containers)",
 "R2122": "Internal exception handling in payload validator",
 "R2455": "Conflicting hook import path; not verified against code",
 "R2496": "Enum merge fact not verifiable from line text",
 "R2207": "Generator type-branch internals",
 "R2210": "Generator request-type branch internals",
 "R2216": "Guice builder sample; runtime module internals",
 "R2419": "Guice builder sample; runtime module internals",
 "R2453": "Broken anchor link in generated doc, not platform behaviour",
 "R2454": "Broken anchor link in generated doc, not platform behaviour",
 "R2538": "Example logic bug in doc sample, not platform behaviour",
 "R2539": "Example logic bug in doc sample, not platform behaviour",
 "R2716": "Transformation internals for table set selector actions",
 "R2764": "Codegen comment escaping edge case",
 "R2580": "JSL grammar internals; fact not verifiable from line",
 "R2373": "JQL grammar tokenisation internals",
 "R2364": "Schema transformation internals",
 "R2130": "Dispatcher AGENTS.md internals",
}

def default_np(r):
    p = r["path"]; repo = r["repo"]
    if "openspec/" in p:
        return "openspec change or archive record, contributor doc"
    if p.endswith("AGENTS.md") or "AGENTS.md" in p:
        return "Module index file for judo-ng internals"
    if repo.startswith("eclipse/"):
        return "Eclipse/EMF plumbing, not application-facing"
    if repo.startswith("packages/"):
        return "Packaging of judo-ng bundles, not application-facing"
    if repo.startswith("tools/"):
        return "judo-ng tooling, not application-facing"
    if repo.startswith("spring/"):
        return "judo-ng plugin internals, no app-facing contract"
    if repo.startswith("models/"):
        return "Metamodel framework internals"
    if repo.startswith("template/"):
        return "Generator internals, no documented app-facing contract"
    if repo.startswith("runtime/"):
        return "Runtime module internals, no app-facing contract"
    return "Framework internals, not application-facing"

verdicts = []
kept = []
ids = []
for r in rows:
    i = r["id"]
    ids.append(i)
    if i in KEEP:
        tgt, fact, ev, already, reason = KEEP[i]
        verdicts.append({"id": i, "verdict": "keep", "reason": reason})
        kept.append({"id": i, "target": "catalog/agent-docs/" + tgt.replace("frontend/../", ""),
                     "fact": fact, "evidence": ev, "already_documented": already})
    elif i in DUP:
        verdicts.append({"id": i, "verdict": "duplicate", "reason": "Same fact as kept " + DUP[i]})
    else:
        reason = NP_OVERRIDE.get(i) or default_np(r)
        verdicts.append({"id": i, "verdict": "not-platform", "reason": reason})

# sanity: dup targets must be kept
for d, k in DUP.items():
    assert k in KEEP, (d, k)
assert len(set(ids)) == len(ids), "duplicate input ids"
assert len(verdicts) == len(rows)

with open(OUT_V, "w", encoding="utf-8") as f:
    for v in verdicts:
        f.write(json.dumps(v, ensure_ascii=False) + "\n")
with open(OUT_K, "w", encoding="utf-8") as f:
    for k in kept:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")

from collections import Counter
c = Counter(v["verdict"] for v in verdicts)
ak = sum(1 for k in kept if k["already_documented"])
print("input", len(rows))
print("keep", c["keep"], "not-platform", c["not-platform"], "duplicate", c["duplicate"])
print("kept rows", len(kept), "already_documented", ak)
print("verdict lines", len(verdicts), "unique ids", len(set(v["id"] for v in verdicts)))
