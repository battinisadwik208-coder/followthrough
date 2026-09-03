# FollowThrough — 5-Minute Demo Video Script

## Before recording

- Use `sample_inquiries/01_clear.txt` in the terminal or dashboard.
- Keep `README.md` open at the Mermaid architecture diagram.
- Ensure the demo shows a real Amazon Nova-generated draft and the visible approval gate.
- Do not claim Gmail/Google Calendar is live: say the demo uses controlled sample inputs and mock calendar slots for recording reliability.

## 0:00–0:30 — Problem

"Freelancers lose good client inquiries because a reply is not one task. You have to read the request, remember relevant work, write a credible proposal, check your calendar, and find time to respond. That can turn into a two-day delay — and the lead may choose someone faster."

## 0:30–0:55 — Who and why

"FollowThrough is for solo consultants, freelance designers and developers, and small service businesses. It removes the repetitive preparation work, but it does not take over the relationship: the human must approve every proposal before it is ready to send."

## 0:55–1:15 — Product overview

"I built FollowThrough with the AWS Strands Agents SDK and Amazon Nova Lite on Bedrock. It parses an inquiry, retrieves relevant real portfolio evidence, drafts a grounded response, proposes call times, and pauses for approval."

## 1:15–3:25 — Live workflow

1. Show the sample inquiry: B2B SaaS marketing-site redesign, budget, six-week timeline, US Eastern timezone.
2. Say: "I trigger FollowThrough with this new inquiry."
3. Show the parsed output: urgency, budget signal, timezone hint.
4. Show portfolio retrieval: the B2B SaaS marketing-site rebuild is selected. Say: "The agent found this past project because it genuinely matches the request. If it found no match, it is instructed not to invent one."
5. Show Amazon Nova generating the proposal draft.
6. Show the three call slots.
7. Highlight the editable draft and approval button/prompt. Say: "This is the critical guardrail. The agent has prepared a response, but it has not emailed anyone. I can edit it, request a revision, or approve it."
8. Approve the draft. Say: "Approval makes the draft ready for the freelancer to send themselves. No automatic email is sent."

## 3:25–4:10 — Architecture

Show the README Mermaid diagram.

"Strands is the orchestrator. Deterministic tools parse the inquiry, retrieve relevant portfolio records, and suggest calendar slots. Amazon Nova Lite on Bedrock drafts the response using only the prepared inquiry and portfolio context. The final tool is the human approval gate. For demo stability I use a JSON portfolio and mock calendar data, and those can later be swapped for S3 and Google Calendar."

## 4:10–4:45 — Impact and differentiation

"FollowThrough targets a real, repeated professional pain: delayed responses to client inquiries. Its value is not another chatbot. It completes the preparation loop end to end, then surfaces only when a professional judgment is needed. That saves time without sacrificing trust or voice."

## 4:45–5:00 — Close

"Next, I would connect Gmail, Google Calendar availability, automated no-reply follow-up drafts, and deploy through Amazon Bedrock AgentCore. Today, FollowThrough already shows the essential agentic workflow: faster client responses with a human still in control."
