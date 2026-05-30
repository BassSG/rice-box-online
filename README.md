# Rice Box Online

Home-kitchen operating website and static PWA for launching a Thai online rice box shop.

## What This Website Includes

- Responsive website for desktop and mobile.
- Mobile app-like bottom navigation.
- Installable PWA manifest, service worker, real app icons, Apple touch icon, maskable Android icon, and install screenshots.
- Generated food images for the Thai core menu.
- Family-friendly 09:00-15:00 selling schedule with 15:00-16:30 child pickup block and after-16:30 Makro prep run.
- Practical shopping list for 30 boxes per day.
- Menu cost, direct price, platform price, and gross profit.
- Low / Mid / High startup capital packages for a kitchen that already has equipment.
- 1, 3, and 6 month forecast.
- Proposal-ready documentation.

## Live Deployment

This repository is designed for GitHub Pages. If GitHub Pages is enabled for the `main` branch, the public URL should be:

https://basssg.github.io/rice-box-online/

## Documents

- [Business Plan](docs/business-plan.md)
- [Operations Manual](docs/ops-manual.md)
- [Costing and Forecast](docs/costing-forecast.md)

## Current Scope

This is a polished static PWA and operating plan. It does not include a real backend, payment gateway, order database, inventory database, or rider tracking API yet.

## Recommended Next PRs

1. Add a real order form that can submit to Google Sheets, Airtable, Supabase, or a backend API.
2. Add a daily sales and ingredient-cost spreadsheet.
3. Add payment flow with a local Thai payment provider or QR payment workflow.
4. Add admin dashboard for kitchen tickets, QC, and delivery status.
5. Replace generated menu photos with real product photography after pilot testing.
