# FollowThrough — Devpost Submission Draft

## Tagline

Turn a new freelance inquiry into a grounded proposal draft and three possible call times — then stop for human approval.

## What it does

FollowThrough is an AI agent for solo consultants, freelancers, and small service businesses that need to respond to client inquiries quickly without outsourcing judgment.

When an inquiry arrives, FollowThrough:

1. extracts the client need, budget signals, urgency, and timezone hints;
2. searches the freelancer's past-project records for the most relevant real examples;
3. uses Amazon Nova Lite on Amazon Bedrock to draft a concise, professional proposal grounded in those examples;
4. suggests exactly three available intro-call times using a demo-stable calendar tool; and
5. stops at a clear human-approval gate. It never sends an email automatically.

The agent turns a workflow that commonly takes a busy freelancer 24–72 hours into a reviewable draft within minutes, while keeping the human responsible for every message that reaches a client.

## The problem

Freelancers and independent consultants frequently lose promising leads because a new inquiry requires several context switches: read the email, understand the request, remember related past work, draft a credible reply, check the calendar, and propose a call. Each individual step is small, but together they create slow responses and lost opportunities.

Generic auto-reply tools are not a safe answer: a fabricated project reference, incorrect price, or wrong tone can damage a client relationship.

## Who it is for

FollowThrough is designed for solo consultants, freelance designers and developers, and small service businesses (1–5 people) that receive client inquiries and need to respond fast without auto-sending AI messages.

## Why it matters

FollowThrough removes the repetitive preparation work while preserving the decision that matters: the human reviews, edits, and approves every draft. It helps a professional be faster without becoming less accountable.

## How it is built

- **Agent framework:** AWS Strands Agents SDK (Python)
- **Model:** Amazon Nova Lite through Amazon Bedrock (`amazon.nova-lite-v1:0`, `us-east-1`)
- **Agent workflow:** deterministic orchestration of inquiry parsing, local portfolio retrieval, Nova proposal drafting, calendar-slot suggestion, and a human approval/revision loop
- **Portfolio store:** local JSON for a repeatable demo; designed to be replaceable with S3 or DynamoDB
- **Experience:** terminal workflow plus a lightweight Streamlit human-review dashboard
- **Safety design:** no email is sent by the agent; approval only marks the draft as ready to send

## Design decision: human approval is a feature

The most important product decision is not to auto-send. FollowThrough makes its reasoning inspectable: the reviewer sees the urgency and budget signals it extracted, the past projects it matched, the proposed slots, and the editable proposal before approving it. This protects a freelancer's voice and client relationships while still saving the repetitive preparation time.

## What is intentionally mocked for the hackathon demo

Calendar availability is demo-stable mock data, so a recording is never broken by OAuth or an unavailable external calendar. Email ingestion is triggered with sample inquiries for the same reason. The core agentic work — retrieval, model drafting, orchestration, and human approval — remains real and observable.

## What comes next

Post-hackathon, FollowThrough can add Gmail ingestion, Google Calendar freebusy queries, S3-backed project history, follow-up suggestions after no reply, and Amazon Bedrock AgentCore Runtime deployment.

## Required links to add before submission

- Public code repository: https://github.com/battinisadwik208-coder/followthrough
- Demo video (public YouTube/Vimeo): `ADD_VIDEO_URL`
- Optional live demo: `ADD_LIVE_DEMO_URL`
