# Story Scout

A weekly editorial scout agent that finds biology + AI stories for your Substack.

Powered by Claude with web search — it scans bioRxiv, Nature, Science, and science news, then delivers 3 story candidates with angles, tensions, and interview leads.

## Setup

```bash
# Install dependencies
make install

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Required API keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) |
| `SENDGRID_API_KEY` | [app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys) (optional) |

If `SENDGRID_API_KEY` is not set, the briefing is saved to `briefing.html` for local preview.

## Usage

### Run manually

```bash
make run
# or
python scout.py
```

### Schedule weekly (every Monday at 8am)

```bash
make cron-install
```

To remove the cron job:

```bash
make cron-uninstall
```

## Output

Each briefing contains 3 stories with:

- **The Story** — what happened, in 1-2 sentences
- **Why Now** — why this matters this week specifically
- **The Missing Angle** — the editorial gap existing coverage isn't filling
- **Who to Talk To** — types of experts worth interviewing
- **Tension/Pushback** — the strongest counterargument

## Project structure

```
scout.py       — main agent logic (runs Claude with web search)
prompt.py      — system prompt and output schema
mailer.py      — HTML email formatting and SendGrid sending
scheduler.py   — cron job management
```
