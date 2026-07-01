---
name: digital-product-indie-site
description: Use when the user wants to build, clone, audit, or preserve a digital product indie site/storefront that can list digital products, collect USD or foreign-currency payments, route to Lemon Squeezy, Payhip, Gumroad, or Stripe checkout, automatically deliver downloads or access instructions, and keep order records. Trigger on Chinese or English requests such as 数字产品独立站, 海外独立站, 收美金, 自动发货, 数字下载店, creator commerce store, digital product storefront, Gumroad/Payhip/Lemon Squeezy style store, or productized template/PDF/course store.
---

# Digital Product Indie Site

## Core Rule

Build a digital product sales loop, not a generic landing page.

The minimum valid result must support:

- Digital product listing
- Product detail page
- Price, license, refund, and delivery terms
- Checkout payment path
- Automatic post-payment delivery
- Download link or access instructions by email
- Order records visible to the seller
- A clear admin or platform management route

Do not classify company registration sites, AI image tools, PDF chat tools, ordinary blogs, generic SaaS dashboards, or homepage-only shells as this product type.

## Start Here

Before building or auditing, read the relevant source material:

- Business definition: `references/docs/01_正确业务定义.md`
- Mature examples: `references/docs/02_成熟网站案例.md`
- Clone blueprint: `references/docs/03_功能复刻蓝图.md`
- Page and data model: `references/docs/04_页面与数据模型.md`
- Implementation routes: `references/docs/05_实施路线.md`
- Acceptance checklist: `references/docs/06_验收清单.md`
- Execution prompt: `references/commands/Codex_Hermes执行命令.md`
- Reference links: `references/sources/reference_links.json`

Use the visual assets when designing or explaining the system:

- `assets/blueprints/01_business_closed_loop.png`
- `assets/blueprints/02_technical_architecture.png`
- `assets/blueprints/03_page_wireframe.png`
- `assets/video_keyframes/video_contact_sheet.jpg`

The original uploaded package is preserved at:

- `assets/original-package/digital_product_indie_site_skillpack_v1.zip`

## Recommended Route

Prefer Route A for the first real version:

1. Create a Lemon Squeezy or Payhip store.
2. Upload one real or test digital product file.
3. Set USD or foreign-currency pricing.
4. Add preview image, product explanation, license, refund, and delivery terms.
5. Publish the product.
6. Copy the platform product or checkout URL.
7. Build the indie-site shell in Next.js, Framer, or Webflow.
8. Make Buy Now buttons route to the hosted checkout.
9. Test successful payment, download page, email delivery, and seller order record.

Use Route B when the user needs a stronger brand shell: Next.js product pages and SEO, while Lemon Squeezy, Payhip, Gumroad, or Stripe handles checkout and delivery.

Use Route C only when scale or control justifies complexity: Next.js, database, checkout API, payment webhook, signed downloads, email delivery, and user account history.

## Build Requirements

For a first-stage web implementation, include:

- Home page
- Product list
- Product detail page
- Buy Now checkout button using a replaceable `checkoutUrl`
- Success page explaining automatic delivery
- FAQ
- License and refund section
- Contact page or support email
- Seller/admin management note linking to the platform dashboard

Product cards must show title, price, description, and tags. Product details must show contents, target users, file format, license scope, refund policy, and delivery method.

## Acceptance Gate

Mark the result complete only when all are true:

1. At least one real or test digital product is listed.
2. The product has a price, preview, explanation, and license terms.
3. Buy Now reaches checkout or a clearly replaceable checkout placeholder.
4. The design explicitly accounts for payment success and automatic delivery.
5. The buyer receives a download link or access instructions by platform email.
6. The seller can see orders and customer email in a dashboard.
7. The process does not require manual file sending order by order.

For static prototypes, state which parts are placeholders and what exact platform setup is needed next.

## Anti-Dust Reuse

When this skill is used, append a short entry to `references/USAGE_LOG.md` with date, task, route chosen, and outcome.

For failures or near misses, append to `references/FAILURE_REVIEW.md` with:

- What drifted from the digital product storefront goal
- Which checklist item failed
- The next-run prevention rule

Before future similar tasks, search this skill first and reuse its references and assets instead of starting from a blank plan.
