# Cost Policy

## Principle

追加課金を発生させない。月額プラン内で回す。

## Allowed

- Claude Code / Codex monthly-plan usage
- Local Markdown / CSV
- Local Python scripts
- Manual X posting
- X Pro scheduling if already available to the user
- GitHub repository management

## Not Allowed Without Explicit Approval

- X API
- OpenAI API key usage outside subscription
- Anthropic API key usage outside subscription
- FireCrawl
- Arcade
- Supabase
- Postiz paid plan
- SocialDog paid plan
- paid analytics dashboard
- browser automation for X actions

## Rationale

The first bottleneck is not automation. The first bottleneck is the lack of a repeatable editorial system.

Therefore, do not pay for automation until the repository can already produce and review posts consistently for four weeks.

## Upgrade Trigger

Consider paid tools only when all conditions are met:

1. 4週間連続で週4本以上投稿できた
2. post_log.csvが埋まっている
3. 伸びる投稿型が最低2つ見えている
4. β募集またはアプリ導線に明確な反応がある
5. 手動作業が明確にボトルネックになっている
