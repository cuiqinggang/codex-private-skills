# Plugin Workflow Matrix

| Capability | Video Plugin / Capability | Good For | Not Good For | External Account | Network | High-Risk Permission | AI Company OS Fit | Priority | Safe Call Pattern |
|---|---|---|---|---|---|---|---|---|---|
| Product Design | Product Design | Product flows, page structure, dashboard planning | Backend mutation or deployment | Maybe | Maybe | Low | Strong | High | Use for brief, routes, screens, and review before build |
| Figma | Figma | Figma-to-code when a real Figma link exists | Tasks without design files | Yes | Yes | Medium | Conditional | High when design exists | Capability check first; inspect read-only before implementation |
| Build Web Apps | Web app building | HTML, CSS, React, Vite, dashboards, acceptance pages | Native mobile-only work | No for local build | Optional | Low | Strong | High | Build locally, validate in browser, then package |
| Chrome / Browser | Chrome, browser testing | Visual checks, console checks, viewport checks | Private account flows without approval | Maybe | Optional | Medium | Strong | High | Prefer local targets; use screenshots and console evidence |
| GitHub | GitHub | Issues, PRs, reviews, versioned collaboration | Unapproved pushes or destructive history changes | Yes | Yes | High | Medium-strong | Medium-high | Read-only first; ask before commits, pushes, merges, or writes |
| Supabase | Supabase | Schema planning, Postgres, auth/RLS design | Unapproved production DB access | Yes | Yes | High | Medium | Medium | Draft schema locally; no real DB changes without approval |
| Deployment | Vercel / Netlify | Preview links, production delivery planning | Unapproved public deployment | Yes | Yes | High | Medium | Medium | Local proof first; request approval before deploy |
| Agentic Workflow | Superpowers / planning / TDD / debug | Complex delivery loops, test-first work, debug closure | Simple one-off answers | No | No | Low | Strong | High | Plan, implement, test, summarize residual risk |
| Build iOS Apps | iOS app building | Mobile app prototypes when requested | Current dashboard and Obsidian web work | Yes/Maybe | Maybe | Medium | Weak now | Low | Only route here when user asks for mobile app |
| Creative Production | Creative Production | Marketing visuals, moodboards, launch assets | Core engineering validation | Maybe | Maybe | Low-medium | Conditional | Medium | Use for visual assets, not as replacement for acceptance proof |
| Data Analysis | Data Analytics | KPI reports, analytics dashboards, data explanation | Unavailable or unaudited data claims | Maybe | Maybe | Medium | Conditional | Medium | Use source-backed data and bounded snapshots |
