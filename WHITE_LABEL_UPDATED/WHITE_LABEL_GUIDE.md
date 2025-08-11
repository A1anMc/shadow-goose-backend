# 🎨 **NAVIMPACT WHITE-LABELING COMPLETE GUIDE**

## 📋 **EXECUTIVE SUMMARY**

This document provides complete instructions for white-labeling the NavImpact platform for any client. The platform is built with a sophisticated branding system that supports multiple clients with different visual identities, team structures, and functional requirements.

**Current Platform Status:**
- ✅ **Backend**: FastAPI with PostgreSQL database
- ✅ **Frontend**: Next.js with Tailwind CSS
- ✅ **Branding System**: Multi-client support
- ✅ **Deployment**: Render platform ready
- ✅ **Features**: Grant management, team collaboration, impact measurement

---

## 🛣️ **PRODUCT ROADMAP**

**Status**: 85% complete • Backend live • Frontend ready to deploy

- **Phase 1 – Foundation**: Complete (API, DB, core features)
- **Phase 2 – Frontend deployment & integration**: In progress (deploy Next.js app, E2E testing)
- **Phase 3 – Authentication & user management**: Planned (login, protected routes, roles, password reset)
- **Phase 4 – Advanced grants & reporting**: Planned (AI matching, deadlines, application tracking, docs; PDF/CSV/export/email/scheduled reports)
- **Phase 5 – Government compliance**: Planned (data access tiers, outcome domains, LGA, SDG mapping, departmental reports, audit trails, accessibility)
- **Phase 6 – Production optimization**: Planned (Redis caching, DB indexing, CDN, load balancing, security hardening, monitoring, backups, DR)

### Progress Tracking

| Phase | Status | Completion | Priority |
|-------|--------|------------|----------|
| Phase 1 | ✅ Complete | 100% | - |
| Phase 2 | 🚧 In Progress | 90% | 🔴 High |
| Phase 3 | ⏳ Planned | 0% | 🟡 Medium |
| Phase 4 | ⏳ Planned | 0% | 🟡 Medium |
| Phase 5 | ⏳ Planned | 0% | 🟢 Low |
| Phase 6 | ⏳ Planned | 0% | 🟢 Low |

**Overall Completion: 85%**

**Next 2 weeks (reference rollout)**
- **Week 1**: Deploy frontend to Render, configure build/start, set env vars, verify health checks, run E2E tests
- **Week 2**: Implement auth (login/logout, protected routes, registration, password reset), initial profiles and roles

**White-label implications**
- **Phase 2 (Deployment)** — Owners: Platform + DevOps; Client provides domain, branding assets, environment values
- **Phase 3 (Auth & Users)** — Owners: Platform + Client Admin; Client provides user list, role matrix, optional SSO details
- **Phase 4 (Grants & Reporting)** — Owners: Platform + Grants Lead; Client provides sample applications, report templates

**Rollout timeline template**
- **T0 (Kickoff)**: Confirm branding, domains, env vars, user/role matrix
- **T+3 days (Staging)**: Branding live on staging; UAT begins
- **T+7 days (Production)**: Go-live; monitoring and support windows active

References:
- Engineering roadmap: [docs/roadmap.md](../docs/roadmap.md)
- White-label product roadmap: [NAVIMPACT_ROADMAP.md](../NAVIMPACT_ROADMAP.md)

## 📄 Client Rollout Brief
- **Objectives**: Launch a branded, secure instance aligned to client OKRs and workflows
- **Scope**: Branding, env/DNS, authentication & roles, grants & reporting, optional integrations
- **Timeline**: Kickoff (T0) → Staging (T+3d) → Production (T+7d)
- **Acceptance**: Branded UI, passing E2E tests, protected routes, reports/exports working
- **Artifacts**: Use the per‑client plan `docs/CLIENT_ROLLOUT_TEMPLATE.md`

## 🔌 Integrations: Slack & Notion (Optional)
- **Slack env**: `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_DEFAULT_CHANNEL`, `SLACK_WEBHOOK_URL`
- **Slack tasks**: Create app/bot, add to channels, map events, test in staging
- **Notion env**: `NOTION_API_KEY`, `NOTION_REDIRECT_URI`, `NOTION_DATABASE_ID_GRANTS`, `NOTION_DATABASE_ID_TASKS`
- **Notion tasks**: Connect workspace (OAuth), map properties, schedule sync, enable logs

## 📊 Analytics & Insights (Overview)
- **Define KPIs** and map to OKRs; publish dashboards (exec, grants, impact)
- **Instrument events** (grant_viewed, task_completed, report_generated)
- **Env**: `NEXT_PUBLIC_ENABLE_ANALYTICS`, `NEXT_PUBLIC_ENV`, `SENTRY_DSN`; confirm `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT`
- See `docs/CLIENT_ROLLOUT_TEMPLATE.md` → Analytics & Insights

## 🧭 Dashboard Navigation & Tabs
- **Insights** (`/insights`): AI Insights Dashboard (model status, grant recommendations, impact analysis)
- **Integrations** (`/integrations`):
  - **Status** (`/integrations/status`): Env/config readiness checks
  - **Slack** (`/integrations/slack`): Setup and test notifications
  - **Notion** (`/integrations/notion`): Connect workspace and map databases
- **Grants** (`/grants`):
  - Existing: AI Matching, Timeline, Feedback, Apply
  - New: **Applications** (`/grants/applications`), **Documents** (`/grants/documents`)
- **Admin** (`/admin`): **Users & Roles**, **Audit Logs**, **Webhooks**
- **Notifications** (`/notifications`): Inbox and preferences
- **Compliance** (`/compliance`): Data export/delete, retention, accessibility (stub)
- **Status** (`/status`): API health overview

Acceptance pointers (UAT):
- [ ] Insights loads with no console errors and shows placeholders if data absent
- [ ] Integrations Status lists required envs; Slack/Notion pages reachable
- [ ] Grants Applications/Documents pages render tables/actions (stubs ok)
- [ ] Admin pages render and are protected once RBAC is enabled
- [ ] Notifications and Compliance pages render; Status shows `/api/health`

## 📦 Client Inputs Checklist
- **Strategic alignment package**: Org mission/vision/values, strategic direction, annual/quarterly OKRs, top priorities; see `docs/CLIENT_ROLLOUT_TEMPLATE.md` → Strategic Alignment & OKRs
- **Phase 2 (Deployment)**: Domains/DNS, branding assets (SVG logos, fonts), environment values (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_CLIENT), staging/prod URLs
- **Phase 3 (Auth & Users)**: User list, role matrix, SSO IdP metadata (optional), privacy/security approvals
- **Phase 4 (Grants & Reporting)**: Sample grant applications, reporting templates, document storage policy

## 👥 Owner Matrix
| Phase | Owners | Client deliverables | Platform deliverables |
|------|--------|----------------------|------------------------|
| 2: Deploy | Platform + DevOps | Domains, branding, env values | Provision services, configure CI/CD |
| 3: Auth | Platform + Client Admin | User list, role matrix, SSO (if any) | Auth flows, protected routes, RBAC |
| 4: Grants/Reports | Platform + Grants Lead | Samples, templates | AI matching, exports, report generation |

## 🔧 Environment & DNS Requirements
- **Frontend**: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_CLIENT`, `NEXT_PUBLIC_APP_NAME`, `NEXT_PUBLIC_APP_VERSION`
- **Backend**: `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY`, `SENTRY_DSN`, `REDIS_URL`, `CORS_ORIGINS`
- **Email branding**: `APP_NAME`, `BRAND_COLOR`, `BRAND_LOGO_URL`
- **DNS**: CNAMEs to Render services for web and API; confirm staging and production hostnames

## ✅ Acceptance Criteria Per Phase
- **Phase 2**: Branded pages load; health endpoints reachable; E2E tests pass; no console errors
- **Phase 3**: Login/logout work; protected routes enforced; roles respected; JWT valid/expiring
- **Phase 4**: Matching returns results; reports generate; CSV/PDF exports succeed; ML endpoints live (`/api/v1/ml-analytics/*`); grant model trained; OKR alignment dashboard populated; AI recommendations visible

## 🚀 Go‑Live Checklist
- Preflight: `scripts/pre_deployment_check.sh`
- Backend health: `scripts/verify-health.sh`
- Deployment verification: `scripts/verify-deployment.sh`
- Post‑deploy monitor: `scripts/post_deployment_monitor.sh`
- Frontend preview for UAT: `cd frontend && npm run preview`

Example (non‑interactive):
```bash
bash scripts/pre_deployment_check.sh --env production
bash scripts/verify-health.sh https://navimpact-api.onrender.com
bash scripts/verify-deployment.sh --web https://navimpact-web.onrender.com --api https://navimpact-api.onrender.com
```

## 🔁 Change Management
- Semantic versioning for client releases
- Maintain a CHANGELOG and release notes for each client rollout
- Document configuration changes and rollback steps

## ✅ Dara Recommendations Checklist
- **ML & OKR Alignment**: Grant model trained; `/api/v1/ml-analytics/*` live; OKR Alignment Dashboard populated; AI recommendations visible
- **Slack Integration**: `SLACK_*` envs set; bot added to channels; task assignment notifications fire in staging
- **Notion Integration**: OAuth connected; `NOTION_*` envs set; database IDs mapped; sync runs and logs visible
- **Analytics**: KPIs defined; dashboards published; `NEXT_PUBLIC_ENABLE_ANALYTICS=true` (when ready); `SENTRY_DSN` configured; core events instrumented
- **Branding**: `NEXT_PUBLIC_CLIENT`, `APP_NAME`, `BRAND_COLOR`, `BRAND_LOGO_URL` applied across UI and email templates
- **Security**: `SECRET_KEY` and `JWT_SECRET_KEY` strong; `CORS_ORIGINS` correct; rate limiting enabled
- **Performance**: Health checks green; p95 latency within SLO; DB indexing verified; background jobs stable
- **Documentation**: `docs/CLIENT_ROLLOUT_TEMPLATE.md` filled per client; support contacts set; rollback plan documented
- **Code Quality (SOLID/DRY)**: Service-layer boundaries respected; no duplicate endpoints; tests pass for critical paths

## .gitignore recommendations (per workspace)

Recommended entries to avoid committing secrets, builds, caches, and local artifacts:

```
# OS/editor
.DS_Store
Thumbs.db
.vscode/
.idea/
*.log

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.venv/
venv/
*.egg-info/
dist/
build/
.pytest_cache/
.mypy_cache/
.cache/
.coverage*
htmlcov/

# Backend env & branding secrets
.env
.env.*


# ML artifacts
app/ml_models/*.pkl
app/ml_models/*.joblib

# Node/Next.js (frontend)
frontend/node_modules/
frontend/.next/
frontend/.turbo/
frontend/.vercel/
frontend/out/
frontend/.eslintcache
frontend/.env
frontend/.env.*

# Legacy/archives (optional)
ARCHIVE/**/node_modules/
ARCHIVE/**/.next/
ARCHIVE/**/out/

# Local databases/backups (if any)
*.db
*.sqlite
backups/
```

Note: SQL migration files in `alembic/versions/` and structured SQL under `scripts/` are intentionally tracked. If you generate ad‑hoc dumps, place them in `backups/` (ignored above).

---

## 🎯 **WHITE-LABELLING PROCESS OVERVIEW**

### **Phase 1: Client Discovery (1-2 days)**
- Gather client requirements and branding assets
- Define team structure and roles
- Identify functional customisations needed

### **Phase 2: Branding Implementation (2-3 days)**
- Update colour palette and typography
- Implement client logo and visual identity
- Customise UI components and layouts

### **Phase 3: Content Customisation (1-2 days)**
- Add client team members and roles
- Configure project types and workflows
- Set up grant matching criteria

### **Phase 4: Testing & Deployment (1-2 days)**
- Test all functionality with new branding
- Deploy to staging environment
- Client review and final deployment

---

## 🎨 **BRANDING SYSTEM ARCHITECTURE**

### **Current Branding Configuration**

The platform uses a sophisticated branding system located in `frontend/src/lib/branding.ts`:

```typescript
export interface BrandingConfig {
  name: string;
  logo: string;
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
```

### **Environment-Based Branding**

The system automatically selects branding based on environment variables:

```typescript
export function getBranding(): BrandingConfig {
  const client = process.env.NEXT_PUBLIC_CLIENT || 'sge';

  switch (client) {
    case 'sge':
    case 'shadow-goose':
      return sgeBranding;
    case 'navimpact':
    default:
      return navimpactBranding;
  }
}
```

---

## 🚀 **CURSOR AI AGENT PROMPTS**

### **Prompt 1: Client Discovery**

```
You are a white-labeling specialist for the NavImpact platform. Your task is to gather comprehensive client requirements for white-labeling.

**Platform Overview:**
- Grant management and impact measurement platform
- Team collaboration and project management
- Built with Next.js frontend and FastAPI backend
- Sophisticated branding system with multi-client support

**Required Information:**
1. **Client Branding:**
   - Company name and logo (SVG preferred)
   - Brand guidelines document
   - Colour palette (primary, secondary, accent, background)
   - Typography requirements (headers, body text)
   - Tone and aesthetic preferences

2. **Team Structure:**
   - Team member list with roles and responsibilities
   - Organisational hierarchy
   - Project assignments and workflows
   - Access permissions and security requirements

3. **Functional Requirements:**
   - Grant focus areas and criteria
   - Project types and workflows
   - Impact measurement frameworks
   - Integration requirements (Notion, etc.)
   - Reporting and analytics needs

**Deliverable:** Create a comprehensive client requirements document with all necessary information for white-labeling.
```

### **Prompt 2: Branding Implementation**

```
You are implementing white-label branding for the NavImpact platform. Use the following specifications to update the branding system.

**Client Requirements:**
[INSERT CLIENT REQUIREMENTS HERE]

**Implementation Tasks:**

1. **Update Branding Configuration:**
   - Modify `frontend/src/lib/branding.ts`
   - Add new client branding configuration
   - Update environment variable handling

2. **Update Tailwind Configuration:**
   - Add client colours to `frontend/tailwind.config.ts`
   - Import client fonts
   - Update colour palette and typography

3. **Update Global Styles:**
   - Modify `frontend/src/app/globals.css`
   - Import client fonts
   - Update CSS variables

4. **Update Components:**
   - Modify `frontend/src/components/layout/Sidebar.tsx`
   - Update `frontend/src/app/(dashboard)/page.tsx`
   - Customize navigation and branding elements

**Technical Requirements:**
- Maintain accessibility standards (WCAG compliance)
- Ensure responsive design works on all devices
- Preserve existing functionality
- Use semantic HTML and proper ARIA labels
- Optimise for performance

**Deliverable:** Implement all branding changes with proper testing and documentation.
```

### **Prompt 3: Content Customization**

```
You are customizing the platform content for a new client. Update the following areas with client-specific information.

**Client Information:**
[INSERT CLIENT TEAM AND PROJECT INFO HERE]

**Customization Tasks:**

1. **Team Management:**
   - Update team member profiles in the system
   - Configure roles and permissions
   - Set up mentorship relationships
   - Add team member photos and bios

2. **Project Configuration:**
   - Define project types and categories
   - Set up workflow templates
   - Configure grant matching criteria
   - Customize impact measurement frameworks

3. **Grant Management:**
   - Update grant focus areas
   - Configure AI matching algorithms
   - Set up automated scraping criteria
   - Customize grant application workflows

4. **Dashboard Customisation:**
   - Update dashboard metrics and KPIs
   - Customise project cards and displays
   - Configure activity feeds
   - Set up client-specific reporting

**Technical Requirements:**
- Maintain data integrity
- Preserve existing functionality
- Ensure proper error handling
- Add comprehensive logging
- Test all customizations thoroughly

**Deliverable:** Complete content customization with proper testing and documentation.
```

### **Prompt 4: Testing and Deployment**

```
You are responsible for testing and deploying the white-labeled platform. Ensure everything works correctly before going live.

**Testing Checklist:**

1. **Branding Verification:**
   - [ ] All pages display correct client branding
   - [ ] Fonts load properly in production
   - [ ] Colour contrast meets accessibility standards
   - [ ] Logo displays correctly across all devices
   - [ ] Branding is consistent across all components

2. **Functionality Testing:**
   - [ ] All navigation links work correctly
   - [ ] Team management features function properly
   - [ ] Grant management system works as expected
   - [ ] Project creation and management works
   - [ ] Impact measurement tools function correctly

3. **Performance Testing:**
   - [ ] Page load times are acceptable
   - [ ] Font loading doesn't cause layout shifts
   - [ ] Images are optimized and load quickly
   - [ ] No console errors or warnings
   - [ ] Mobile responsiveness works correctly

4. **Accessibility Testing:**
   - [ ] WCAG 2.1 AA compliance
   - [ ] Keyboard navigation works
   - [ ] Screen reader compatibility
   - [ ] Color contrast ratios meet standards
   - [ ] Focus indicators are visible

**Deployment Steps:**
1. Deploy to staging environment
2. Run comprehensive tests
3. Get client approval
4. Deploy to production
5. Monitor for issues
6. Provide client training

**Deliverable:** Complete testing report and successful production deployment.
```

---

## 🛠️ **TECHNICAL IMPLEMENTATION GUIDE**

### **Step 1: Update Branding Configuration**

**File: `frontend/src/lib/branding.ts`**

```typescript
// Add new client branding
export const clientBranding: BrandingConfig = {
  name: "Client Name",
  logo: "Client Logo",
  colors: {
    primary: "#CLIENT_PRIMARY_COLOR",
    secondary: "#CLIENT_SECONDARY_COLOR",
    accent: "#CLIENT_ACCENT_COLOR",
    background: "#CLIENT_BACKGROUND_COLOR",
  },
  fonts: {
    heading: "Client Heading Font",
    body: "Client Body Font",
  },
};

// Update getBranding function
export function getBranding(): BrandingConfig {
  const client = process.env.NEXT_PUBLIC_CLIENT || 'default';

  switch (client) {
    case 'client-name':
      return clientBranding;
    case 'sge':
      return sgeBranding;
    case 'navimpact':
    default:
      return navimpactBranding;
  }
}
```

### **Step 2: Update Tailwind Configuration**

**File: `frontend/tailwind.config.ts`**

```typescript
colors: {
  // Client-specific colors
  'client-primary': '#CLIENT_PRIMARY_COLOR',
  'client-secondary': '#CLIENT_SECONDARY_COLOR',
  'client-accent': '#CLIENT_ACCENT_COLOR',
  'client-background': '#CLIENT_BACKGROUND_COLOR',

  // Keep existing colors for fallback
  primary: { /* existing */ },
  // ... other existing colors
},
fontFamily: {
  'client-heading': ['Client Heading Font', 'serif'],
  'client-body': ['Client Body Font', 'sans-serif'],
  // ... existing fonts
},
```

### **Step 3: Update Global Styles**

**File: `frontend/src/app/globals.css`**

```css
/* Import client fonts */
@import url('https://fonts.googleapis.com/css2?family=ClientFont:wght@300;400;500;600;700&display=swap');

/* Client CSS variables */
:root {
  --client-primary: #CLIENT_PRIMARY_COLOR;
  --client-secondary: #CLIENT_SECONDARY_COLOR;
  --client-accent: #CLIENT_ACCENT_COLOR;
  --client-background: #CLIENT_BACKGROUND_COLOR;
}

/* Client-specific styles */
.client-branded {
  background: linear-gradient(135deg, var(--client-primary) 0%, var(--client-secondary) 50%, var(--client-accent) 100%);
  color: var(--client-background);
}
```

### **Step 4: Update Components**

**File: `frontend/src/components/layout/Sidebar.tsx`**

```typescript
// Import branding
import { getBranding } from '../../lib/branding';

export default function Sidebar() {
  const branding = getBranding();

  return (
    <div className={`bg-gradient-to-br from-${branding.colors.primary} to-${branding.colors.secondary}`}>
      <div className="flex items-center space-x-3">
        <img src={branding.logo} alt={branding.name} className="w-6 h-6" />
        <span className={`text-lg font-bold font-${branding.fonts.heading}`}>
          {branding.name}
        </span>
      </div>
      {/* Rest of sidebar content */}
    </div>
  );
}
```

---

## 📊 **CLIENT ONBOARDING TEMPLATE**

### **Client Information Gathering**

**Branding Requirements:**
- [ ] Company name and tagline
- [ ] Logo files (SVG preferred, PNG fallback)
- [ ] Brand guidelines document
- [ ] Colour palette specifications
- [ ] Typography requirements
- [ ] Tone and aesthetic preferences
- [ ] Icon style preferences

**Team Structure:**
- [ ] Team member list with roles
- [ ] Organisational hierarchy
- [ ] Project assignments
- [ ] Mentorship relationships
- [ ] Access permissions
- [ ] Team member photos and bios

**Functional Requirements:**
- [ ] Grant focus areas
- [ ] Project types and workflows
- [ ] Impact measurement frameworks
- [ ] Integration requirements
- [ ] Reporting needs
- [ ] Custom features needed

### **Implementation Checklist**

**Phase 1: Setup (1-2 days)**
- [ ] Create client branch
- [ ] Update branding configuration
- [ ] Import client fonts
- [ ] Update Tailwind config
- [ ] Set up environment variables

**Phase 2: Design (2-3 days)**
- [ ] Redesign dashboard with client branding
- [ ] Update navigation and sidebar
- [ ] Customise team and profile pages
- [ ] Apply consistent styling across components
- [ ] Test responsive design

**Phase 3: Content (1-2 days)**
- [ ] Add client team members
- [ ] Set up project assignments
- [ ] Configure grant matching criteria
- [ ] Customise impact measurement frameworks
- [ ] Set up client-specific workflows

**Phase 4: Testing (1 day)**
- [ ] Test all functionality with new branding
- [ ] Verify font loading in production
- [ ] Check accessibility compliance
- [ ] Performance testing
- [ ] Cross-browser testing

**Phase 5: Deployment (1 day)**
- [ ] Deploy to staging environment
- [ ] Client review and feedback
- [ ] Deploy to production
- [ ] Client training and handover
- [ ] Documentation delivery

---

## 🎯 **SUCCESS CRITERIA**

### **Branding Success:**
- ✅ Client logo displays correctly across all pages
- ✅ Colour scheme is consistent and accessible
- ✅ Typography loads properly and looks professional
- ✅ Branding feels cohesive and on-brand
- ✅ No visual inconsistencies or broken elements

### **Functionality Success:**
- ✅ All navigation and features work correctly
- ✅ Team management functions as expected
- ✅ Grant management system operates properly
- ✅ Impact measurement tools function correctly
- ✅ Performance remains optimal

### **Client Satisfaction:**
- ✅ Platform feels like their own product
- ✅ All requested customizations are implemented
- ✅ Client team can use the platform effectively
- ✅ Platform meets all functional requirements
- ✅ Client is ready to go live

---

## 🚨 **TROUBLESHOOTING GUIDE**

### **Common Issues and Solutions:**

**Font Loading Issues:**
```css
/* Ensure fonts load properly */
@font-face {
  font-family: 'ClientFont';
  src: url('/fonts/client-font.woff2') format('woff2');
  font-display: swap;
}
```

**Colour Contrast Issues:**
```typescript
// Use Tailwind's contrast utilities
className="text-white bg-black" // High contrast
className="text-gray-900 bg-gray-100" // Medium contrast
```

**Responsive Design Issues:**
```typescript
// Use Tailwind's responsive prefixes
className="w-full md:w-1/2 lg:w-1/3"
```

**Performance Issues:**
- Optimise images and fonts
- Use proper caching strategies
- Minimise bundle size
- Implement lazy loading

---

## 📈 **MONITORING AND MAINTENANCE**

### **Post-Deployment Monitoring:**
- Monitor for any branding inconsistencies
- Track performance metrics
- Monitor user feedback
- Check for accessibility issues
- Monitor error rates

### **Ongoing Maintenance:**
- Regular branding updates
- Performance optimisations
- Security updates
- Feature enhancements
- Client training and support

---

## 🎉 **CONCLUSION**

This white-labeling system provides a robust, scalable solution for customizing the NavImpact platform for any client. The modular architecture ensures that branding changes don't affect core functionality, while the comprehensive testing process guarantees a high-quality end product.

**Key Benefits:**
- ✅ Rapid client onboarding (5-7 days)
- ✅ Consistent quality across all clients
- ✅ Scalable architecture
- ✅ Comprehensive testing
- ✅ Professional delivery

**Next Steps:**
1. Use the provided prompts with your Cursor AI agent
2. Follow the implementation checklist
3. Test thoroughly before deployment
4. Monitor post-deployment performance
5. Provide ongoing support and maintenance

---

## 📞 Support
- Email and Slack support channels per client contract
- Incident response: SEV levels and response times documented in SLOs
- Monitoring: Sentry alerts, deployment monitors, weekly health review

## 📎 Appendix: Templates

### Role matrix (example)
| Role | Permissions | Notes |
|------|-------------|-------|
| Admin | Full access; manage users and roles | Client owner(s) |
| Manager | Create/edit projects, approve tasks | Team leads |
| User | View/edit assigned items | Staff |

### Branding asset checklist
- SVG/PNG logos (dark/light)
- Brand colors (hex)
- Typography (webfont files or names)
- Favicon and social preview images

### UAT sign‑off checklist
- Branding consistent across pages
- Auth flows work for target roles
- Key reports/export verified
- Performance acceptable on target devices

---

**Document Version:** 1.0
**Last Updated:** August 7, 2025
**Prepared by:** Alan McCarthy
**Platform:** NavImpact V2
