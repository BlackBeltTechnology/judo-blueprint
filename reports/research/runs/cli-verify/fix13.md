# Fix #13 verification: CLI `validate` vs Maven UI validation

Gap: webshop R18-6 / R19-1 (`~/Projects/webshop-test/GAPS.md`). After `fill` on the derived singleton access `webshop::PrivacyInfo`, the operation forms `exportMyData` (INSTANCE, file output) and `pollPush` were placed in `PrivacyInfo_View_Edit`. `validate` said `passed ui`; Maven failed in "Verify UI model is presented".

Expected if fixed: new CLI fails like Maven; old CLI passes.

## Setup

- Worktree: `git -C ~/Projects/webshop-test worktree add /tmp/ws-r186 HEAD` (HEAD `71b7829`, model clean, PrivacyInfo exists, `exportMyData` defined on PrivacyInfo but not placed in the view).
- Reproduced the failing state with the old CLI, as the session did:
  - `java -jar /tmp/judo-cli-old.jar -m model/webshop.model fill webshop::PrivacyInfo` (log: `fill-old.log`; created OperationForm for ackPush, eraseAccount, exportMyData, pollPush, subscribePush)
  - `java -jar /tmp/judo-cli-old.jar -m model/webshop.model save` (log: `save-old.log`)
- Daemon stop: `server stop -f` (the bare `stop` subcommand does not exist). `server status` afterwards: Not running.

## 1. Old CLI (`/tmp/judo-cli-old.jar`, 1.1.0.20261109_213146_746dc745_develop)

Command: `java -jar /tmp/judo-cli-old.jar -m model/webshop.model validate`
- exit 0
- `passed esm`, `passed ui`, `passed transform`
- `Validation complete: 0 errors, 2 warnings` (PrincipalHasNoRelationsAndOperations, FeaturedActionsValueIsValid)
- Log: `validate-old.log`

**Verdict: PASS (does not reproduce the gap).**

## 2. New CLI (`target/judo-cli.jar`, 1.1.0.20261119_155735_a64aa981_develop)

Command: `java -jar target/judo-cli.jar -m model/webshop.model validate`
- exit 1
- `passed esm`, then no `passed ui`, then `passed transform`
- UI errors printed:
  - `error ui ActionContainerSameWithActionDefinition ... PrivacyInfo::PrivacyInfo_View_Edit::exportMyData::OperationFormCallAction`
  - `error ui ActionContainerSameWithActionDefinition ... PrivacyInfo::PrivacyInfo_View_Edit::pollPush::OperationFormCallAction`
  - `error ui NamedElementHaveToBeInApplication ParameterlessCallOperationActionDefinition PrivacyInfo::PrivacyInfo_View_Edit::exportMyData::ViewOperation`
  - `error ui NamedElementHaveToBeInApplication ParameterlessCallOperationActionDefinition PrivacyInfo::PrivacyInfo_View_Edit::pollPush::ViewOperation`
- Also XMI ID COLLISION warnings for Admin TabularReferenceField* actions (also present in Maven output).
- Summary line still says `Validation complete: 0 errors, 2 warnings`. The UI errors are printed but not counted in the summary. This is a second problem: the summary contradicts the exit code.
- Log: `validate-new.log`

**Verdict: FAIL (reproduces the gap; matches Maven).**

## 3. Maven frontend-react model step (offline)

Command (in worktree): `cd application/frontend-react/model && mvn -o install -DskipTests -DuseCache=false -DvalidateModels=true`
- Used `mvn` rather than `mvnd`, and no `-am`: the step runs from this module and the plugin is resolved from `~/.m2` (1.1.0.20261109_211802_9d130d8d_develop). `timeout` is not available on this macOS shell.
- exit 1, `BUILD FAILURE`
- `Work 'Verify UI model is presented' has failed`
- Errors:
  - `ActionContainerSameWithActionDefinition` for `PrivacyInfo ... exportMyData::OperationFormCallAction` and `pollPush::OperationFormCallAction`
  - `NamedElementHaveToBeInApplication: PrivacyInfo::PrivacyInfo_View_Edit::exportMyData::ViewOperation`
  - `NamedElementHaveToBeInApplication: PrivacyInfo::PrivacyInfo_View_Edit::pollPush::ViewOperation`
- Log: `maven-frontend-react-model.log`

**Verdict: FAIL (same four errors as the new CLI).**

## Conclusion

The new CLI reports the same UI errors as Maven and exits 1; the old CLI passes `ui` and exits 0. Fix #13 is confirmed for the error detection and exit code. Open issue: the new CLI's summary line still reports `0 errors`.

## Cleanup

- `git -C ~/Projects/webshop-test worktree remove --force /tmp/ws-r186` and `worktree prune`; `worktree list` shows only `~/Projects/webshop-test`. `~/Projects/webshop-test` was not modified.
- Logs copied here from `/tmp/cli-verify/`.
