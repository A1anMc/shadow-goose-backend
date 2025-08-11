# Shadow Goose — Frontend Branding Implementation

Use these edits to enable `NEXT_PUBLIC_CLIENT=shadow-goose` branding.

## 1) Assets
- Place files under `frontend/public/clients/shadow-goose/`:
  - `logo-light.svg`
  - `logo-dark.svg`
  - `favicon.png`
  - `social.png`

## 2) Branding config (`frontend/src/lib/branding.ts`)
```ts
export interface BrandingConfig {
  name: string;
  logoLight: string;
  logoDark: string;
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
  };
  fonts: {
    heading: string;
    body: string;
  };
}

export const shadowGooseBranding: BrandingConfig = {
  name: "Shadow Goose Entertainment",
  logoLight: "/clients/shadow-goose/logo-light.svg",
  logoDark: "/clients/shadow-goose/logo-dark.svg",
  colors: {
    primary: "#1A1A1A",
    secondary: "#FFFFFF",
    accent: "#FF6600",
    background: "#F5F5F5",
  },
  fonts: {
    heading: "Poppins",
    body: "Open Sans",
  },
};

export function getBranding(): BrandingConfig {
  const client = process.env.NEXT_PUBLIC_CLIENT || "navimpact";
  switch (client) {
    case "shadow-goose":
      return shadowGooseBranding;
    // case "sge": return sgeBranding;
    // default:
    default:
      return shadowGooseBranding;
  }
}
```

## 3) Tailwind colors (`frontend/tailwind.config.ts`)
```ts
// ... existing code ...
export default {
  // ... existing code ...
  theme: {
    extend: {
      colors: {
        sg: {
          primary: "#1A1A1A",
          secondary: "#FFFFFF",
          accent: "#FF6600",
          background: "#F5F5F5",
        },
      },
      fontFamily: {
        heading: ["Poppins", "ui-sans-serif", "system-ui"],
        body: ["Open Sans", "ui-sans-serif", "system-ui"],
      },
    },
  },
};
```

## 4) Global fonts (`frontend/src/app/globals.css`)
```css
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&family=Poppins:wght@400;600;700&display=swap');

:root {
  --sg-primary: #1A1A1A;
  --sg-secondary: #FFFFFF;
  --sg-accent: #FF6600;
  --sg-background: #F5F5F5;
}

html, body { font-family: var(--font-body, 'Open Sans'), ui-sans-serif, system-ui; }
.sg-heading { font-family: var(--font-heading, 'Poppins'), ui-sans-serif, system-ui; }
```

## 5) Example usage (`frontend/src/components/layout/Sidebar.tsx`)
```tsx
import Image from "next/image";
import { getBranding } from "@/lib/branding";

export default function Sidebar() {
  const branding = getBranding();
  return (
    <aside className="h-full w-64 bg-[var(--sg-primary)] text-[var(--sg-secondary)]">
      <div className="flex items-center gap-3 p-4">
        <Image src={branding.logoLight} alt={branding.name} width={28} height={28} />
        <span className="sg-heading text-lg font-semibold">{branding.name}</span>
      </div>
    </aside>
  );
}
```

## 6) Env
Ensure in Render (staging and prod):
- `NEXT_PUBLIC_CLIENT=shadow-goose`
- `NEXT_PUBLIC_APP_NAME=Shadow Goose Entertainment`

Optional (after custom domains): update `NEXT_PUBLIC_API_URL`, `CORS_ORIGINS`, and `FRONTEND_URL`.

## 7) Email branding
- Keep `BRAND_LOGO_URL` empty for now. When the final email-safe logo URL is ready, set it in env, and test email templates rendering.

## 8) QA checklist
- All pages show Shadow Goose colors and fonts
- Logos render crisp on light/dark backgrounds
- No console errors; font requests succeed
- Mobile nav/Sidebar looks correct; contrast meets AA
