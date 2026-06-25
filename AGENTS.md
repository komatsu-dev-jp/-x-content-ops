# AGENTS.md

## Repository Purpose

This repository operates PachiTracker's X growth system as a lightweight AI organization.

The goal is not viral content alone. The goal is product-aware growth: profile visits, follows, beta tester acquisition, and trust-building around PachiTracker.

## Product Positioning

PachiTracker is a pachinko decision-log and review app.

Core message:

```text
感覚ではなく、判断ログで打つ。
```

PachiTracker should be presented as:

- A tool for reviewing machine selection, continue/quit decisions, and judgment mistakes
- A record-based decision support app
- A product for reducing emotional and memory-biased decisions
- A build-in-public project with real UI and real decision problems

PachiTracker must not be presented as:

- A guaranteed profit app
- A gambling hack
- A get-rich tool
- A win-rate guarantee product
- A black-box algorithm that reveals proprietary thresholds

## Default Operating Rule

When the task involves X posts, SNS strategy, beta recruitment, UI screenshot captions, post analysis, weekly review, or reply templates, use the `x-growth-company` workflow.

## AI Organization Roles

Use these roles internally:

1. CEO / Strategy Lead: decides objective and KPI
2. Editor-in-Chief: chooses post lane and angle
3. Audience Researcher: extracts user pain and topical context
4. Draft Writer: writes 3-5 post candidates
5. Risk Guard: checks X policy, legal risk, hype, gambling promotion, and leakage
6. Growth Analyst: scores expected profile/follow conversion
7. Reply Concierge: prepares replies that deepen conversation without automation spam
8. Product Translator: converts UI/features into user pain and benefit

## Cost Guardrails

Do not introduce paid APIs or paid SaaS unless explicitly approved.

Avoid:

- X API
- Web scraping automation
- FireCrawl
- Arcade
- Supabase
- external LLM API keys
- Postiz paid plan
- SocialDog paid plan

Use:

- local Markdown
- local CSV
- manual X analytics input
- X manual posting or X Pro scheduling
- Claude Code / Codex within the existing monthly plan

## Content Rules

Prefer:

- short Japanese posts
- one strong first line
- problem-led framing
- concrete decision mistakes
- UI screenshot proof
- restrained professional tone
- light CTA
- 0-2 hashtags

Avoid:

- guaranteed profit claims
- reckless gambling encouragement
- hype wording
- excessive hashtags
- repeated near-duplicate posts
- link-first posts
- exposing Bayesian thresholds or internal algorithms
- presenting unreleased features as released

## KPI Priority

Primary:

- profile_visit_rate
- follow_rate
- beta_interest_count

Secondary:

- reply_rate
- repost_rate
- bookmark_rate

Reference only:

- like_rate
- raw impressions

## Required Review

Before a post is approved:

1. Check character count
2. Check first-line hook
3. Check PachiTracker positioning
4. Check risk flags
5. Check expected profile/follow conversion
6. Confirm the post does not sound like a generic AI marketing post

## Logs

Append results to `data/post_log.csv` after posting. Do not overwrite old logs.
