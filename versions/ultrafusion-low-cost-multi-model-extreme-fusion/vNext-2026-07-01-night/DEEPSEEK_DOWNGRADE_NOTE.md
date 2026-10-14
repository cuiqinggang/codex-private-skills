# DeepSeek Downgrade Note

## Decision

DeepSeek is no longer an official core model in UltraFusion vNext.

## Reasons

1. Fast mode can search the web, but depth is insufficient.
2. Expert/deep-thinking mode reasons well, but cannot search the web.
3. Extreme tasks require a two-step process.
4. Long-term official use would be too cumbersome.
5. This skill needs fewer steps, high quality, and a durable workflow.

## Preserved Uses

- Free testing
- Pure reasoning backup
- Low-cost reverse-review backup

## Backup Flow When Search Is Required

1. Use fast mode to collect facts, links, prices, rules, and current information.
2. Feed the collected material into expert/deep-thinking mode.
3. Use expert mode for reasoning, rebuttal, and gap checks.
4. Send the result to GPT for final fusion.
