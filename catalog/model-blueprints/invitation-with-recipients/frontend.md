## Frontend guidance

### Filter the role choices in the invite dialog

An invite form often lets the inviter pick a role. Not every inviter may grant every role. Filter the role choices in a dialog form action hook (the platform's enumeration filtering hook filters dropdown options from the form data), using the inviter's role and the organization context from the owner data.

### Use a role-to-invitable-roles mapping

Keep the rule in one mapping from the inviter's role to the roles that role may grant. The filter function then reads the mapping. Keeping the rule in data makes it easy to review.

### Distinguish the admin organization from others

The same role can have different rights in its own admin organization and in another organization. Pass the organization flag into the filter, and check it before applying the mapping.

### Filtering is a UI convenience, not enforcement

The hook only narrows what the dropdown offers. A client can still send any value. The invite operation is a custom operation, so no interceptor guards it: check the inviter's right to grant the chosen role inside the operation. For relation-valued choices a range interceptor (it fires only for reference range operations) is the platform's server-side filter.

### Use the generated hook key

Register the hook with the key the framework generates for the dialog and its page. Do not copy the key from another page.

### Keep the container hook thin

A container-level hook for the same form may be needed for a second field. Keep it thin, and move the decision to the dialog-level hook, which has the owner data.

## Examples

### mlszksz-platform

- A dialog form action hook on the organization admin panel's invite form filters the role dropdown. It reads the inviter's role and the admin-organization flag from the owner data, then applies a role-to-invitable-roles mapping.
- The filter separates a platform admin inviting into their own admin organization from a platform admin inviting into another company's panel.
