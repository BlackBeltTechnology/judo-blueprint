---
id: binary-blob-url-hook
title: Binary Token to Object URL Hook
description: "A React hook that downloads a binary attribute through the generated access service and returns an object URL for img, video or embed elements, revoking the previous URL on change and on unmount, with a cancellation flag against late state updates."
aliases: [blob url hook, binary preview hook]
keywords: [blob, object url, createObjectURL, revokeObjectURL, binary token, download, hook, image preview, cleanup]
tags: ["domain:frontend", "layer:frontend", "project:mlszksz-platform", "status:single-project"]
category: component
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/frontend-react/mlszkszplatform__services__mlszksz/src/custom/hooks/useBlobUrl.ts"]
alternatives: [pdf-preview-inline-display]
related: [filestore-mediated-file-transfer, custom-component-directory, pdf-preview-inline-display]
fragment: "none: frontend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Show a stored binary (image, document) inside custom views where the generated widgets are not used. The file download needs the token header, so a plain `src` link to the file cannot work; the hook fetches the bytes and hands the view a local object URL.

## Practice

### Platform base

- Binary attributes hold a token, and the generated access service downloads the file with the token and a disposition (`inline` or `attachment`) ([custom attachments: token flow](../../agent-docs/frontend/advanced-patterns.md)). The download path is a separate authenticated request, so it cannot be used directly as an element `src` (*verify* for your generated version).

### Project practice: one hook owns the URL lifecycle (mlszksz-platform)

- The hook takes a token (or nothing) and returns a string URL or `null`. It creates the access service once with `useMemo`, using the project's shared axios provider.
- The effect first revokes the URL held in a ref, then, if there is a token, downloads in `inline` mode, wraps the response data in a `Blob` with the response content type and stores the new object URL in the ref and in state.
- A local `cancelled` flag is set in the effect cleanup; a response arriving after a token change or unmount does not set state.
- Cleanup revokes the URL held in the ref. The ref, not the state value, is used so the cleanup always sees the latest URL.
- Errors are logged and the hook returns `null`; the caller shows a placeholder.

```typescript
export function useBlobUrl(token: unknown | null | undefined): string | null {
  const [url, setUrl] = useState<string | null>(null);
  const service = useMemo(() => new AccessService(axiosProvider), []);
  const urlRef = useRef<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (urlRef.current) { URL.revokeObjectURL(urlRef.current); urlRef.current = null; }
    if (!token) { setUrl(null); return; }
    (async () => {
      try {
        const res = await service.downloadFile(token, 'inline');
        if (cancelled || res?.status !== 200) return;
        const objectUrl = URL.createObjectURL(new Blob([res.data], { type: res.headers['content-type'] }));
        urlRef.current = objectUrl;
        setUrl(objectUrl);
      } catch {
        if (!cancelled) setUrl(null);
      }
    })();
    return () => {
      cancelled = true;
      if (urlRef.current) { URL.revokeObjectURL(urlRef.current); urlRef.current = null; }
    };
  }, [token, service]);

  return url;
}
```

## Rationale

Object URLs keep the blob in memory until revoked, so every create needs a matching revoke. Centralizing this in one hook keeps views free of leaks and stale updates. The cost is that the whole file is held in memory and downloaded again per mounted view; nothing is cached.

## Example

mlszksz-platform uses the hook in its custom views to render uploaded images from the binary token of the displayed record.

## When to avoid

- The user should save the file; use the generated `downloadFile` helper in attachment mode.
- Large files or video streams; an object URL needs the full body first.
- The generated image or file widgets already show the binary.

## Related

- [[filestore-mediated-file-transfer]] — the backend token flow that produces the tokens
- [[pdf-preview-inline-display]] — opening an inline download in the browser instead
- [[custom-component-directory]] — where such hooks and components live
