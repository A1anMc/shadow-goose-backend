# Shadow Goose Branding PR Bundle

Drop-in edits for the frontend app. Apply these:

1) Add `src/lib/branding.shadow-goose.ts` and import `shadowGooseBranding` into your branding module. In your `getBranding()` switch, map `shadow-goose` to `shadowGooseBranding`.
2) Merge `tailwind.extend.shadow-goose.ts` into `tailwind.config.ts` `theme.extend`.
3) Merge `globals.shadow-goose.css` into `src/app/globals.css` (fonts + CSS variables).
4) Place assets in `public/clients/shadow-goose/`.
5) Ensure envs in Render: `NEXT_PUBLIC_CLIENT=shadow-goose`, `NEXT_PUBLIC_APP_NAME=Shadow Goose Entertainment`.

Files in this bundle:
- src/lib/branding.shadow-goose.ts
- tailwind.extend.shadow-goose.ts
- src/app/globals.shadow-goose.css
- components/sidebar.example.tsx (reference)
- public/clients/shadow-goose/ (assets placeholder)
