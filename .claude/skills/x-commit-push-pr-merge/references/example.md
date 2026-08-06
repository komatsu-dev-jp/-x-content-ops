# x-commit-push-pr-merge: Usage Example

## Scenario: Multi-file changes with skill modification

This example demonstrates how to use the `x-commit-push-pr-merge` skill when making changes to the skill itself plus supporting documentation.

### Setup

1. Make changes to multiple files:
   - Modify SKILL.md (add test log entry)
   - Create references/example.md (this file)

2. Stage the changes:
   ```bash
   git add .claude/skills/x-commit-push-pr-merge/SKILL.md
   git add .claude/skills/x-commit-push-pr-merge/references/example.md
   ```

### Workflow

1. Call the skill: `/x-commit-push-pr-merge`
2. Provide commit message: "Improve: enhance skill docs and add example guide"
3. Wait for PR to be created
4. Open PR in GitHub and click Merge
5. Return and type: "merged"
6. Skill records merge log and suggests /clear

### Expected Output

- PR created with multi-file changes
- Merge log entry recorded with PR#, SHA, timestamp
- Both files successfully committed

### Verification

- Check output/prs/merge-log.md for entry
- Verify git log shows merge commit
- Branch is up to date with origin
