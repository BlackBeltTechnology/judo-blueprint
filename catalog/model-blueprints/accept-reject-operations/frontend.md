## Frontend guidance

### Show accept and reject only for open requests

The generated operation buttons use the guard attributes of the transfer object. Derive the guard from the status, so the buttons appear only while the request is pending. No custom button is needed for the basic case.

- Use one derived boolean per operation (for example, an accept-available flag) and bind it to the button's enabled or hidden state. Caveat: in a multi-button FAB group, a non-featured button in the speed-dial menu does not apply the hidden guard; only featured buttons do. Check the generated fragment before relying on it.
- The guard only controls the UI. The operation itself must still refuse a request that is not pending.

### Pre-filter the approval table

Approval tables should list only the requests that still need a decision. Prefer to solve this in the model: expose a pending-only relation (a derived relation filtered by status) on the transfer object and bind the approval table to it. That works on every page that shows the table.

- A page action hook is the fallback. The agent-docs describe an optional post-refresh handler on the page actions hook (it runs after the refresh, so it reacts to the loaded data); they do not document a pre-refresh filter, so check the generated customization files of the page before relying on it.
- Generated hook keys are per page or container (names ending in the actions hook interface key). Look up the key for the page you extend; do not copy a fixed constant.
- If the same table appears on two pages, register the same hook in both.

### Ask for a reason on reject

The reject operation takes a RejectInput. Its dialog should show one text field for the reason. Make the field required when the domain needs a reason.

## Examples

### Variant seen in practice

- Framework: React.
- Both the embedded admin table and the standalone registration-request table add a status filter in their refresh action hook (custom code), so admins only see verified requests.
- The accept and reject buttons use the generated UI, with the guard attributes controlling visibility.
