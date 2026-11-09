## Frontend guidance

The platform's file utility resolves a download token to a URL and lets the browser open or save it. In a Capacitor app the browser path does not give the user a visible file, so this pattern replaces the save step on native platforms only. The helper modules are project code; their names are examples.

### Replace only the file utility module

The generated file utility is overridden by listing it in the generator-ignore file. The override keeps the same exports, so screens that import the utility keep working. A second module can re-export the override under a project path for custom views.

### Branch on the platform

When the app runs as a native platform, save the file to the device's download folder through the filesystem plugin. On the web, the generated browser download runs unchanged.

### Save as base64

The filesystem plugin writes base64 text, so convert the downloaded blob first. Use an array buffer and a byte loop, then the base64 encoder, rather than a string conversion that corrupts binary data.

```ts
export async function blobToBase64(blob: Blob): Promise<string> {
  const bytes = new Uint8Array(await blob.arrayBuffer());
  let binary = "";
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary);
}
```

### Notify and open

After the save succeeds, show a local notification with the file name. When the user taps it, open the file with the file-opener plugin. Map the file extension to a MIME type for the opener, and fall back to a generic type for unknown extensions.

### Scoped storage

On Android 10 and later, writing to the download folder through scoped storage needs no extra permission. Check the target Android version before adding a storage permission.

### Inline preview is separate

A PDF preview that uses the inline mode of the platform utility is not a native save. Keep the inline preview on the web and in native apps alike, and use the save path only for a download action.
