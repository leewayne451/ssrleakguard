SSRLeakGuard

Server‑side rendering blurs the boundary between server‑only and client‑visible data.

Even when authentication and APIs are correctly implemented, SSR logic can accidentally:


- Serialize sensitive data into HTML responses

- Expose different data to different users unintentionally

- Allow personalized pages to be cached and reused across users

SSRLeakGuard helps surface these hidden SSR‑specific risks.

---

Project Phases

SSRLeakGuard is structured into two phases, each targeting a distinct SSR security problem.


Phase 1 — SSR Data Exposure Detection


Detects sensitive or server‑only data embedded in SSR output, including:

- Emails and other PII

- Authorization roles

- Internal identifiers

- Tokens or configuration values

This phase inspects both rendered HTML and structured SSR hydration data to identify information that should not be sent to the client, even if it is not visibly displayed.

---

Phase 2 — Authorization Inconsistency Detection

Compares SSR responses across different authorization contexts (for example, guest vs authenticated users).


By replaying the same SSR request with different cookies or session states, SSRLeakGuard detects:

- Data visible only to certain users

- Privilege‑related inconsistencies

- Cross‑user SSR data exposure risks

This phase focuses on who receives what data, rather than whether authentication itself is correct.

---

Requirements

System Requirements

- Python 3.8+

- Node.js 18+

- npm (bundled with Node.js)

Supported Frameworks

Next.js (Pages Router)

---

Setup Instructions

1. Clone the repository

	git clone https://github.com/YOUR_USERNAME/ssrleakguard.git
	cd ssrleakguard

---

2. Create a Python virtual environment

	python -m venv venv

Activate the environment:

Windows (PowerShell):

	venv\Scripts\activate

Windows (Command Prompt):

	venv\Scripts\activate.bat

macOS / Linux:

	source venv/bin/activate

---

3. Install dependencies

	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

Verify installation:

	ssrleakguard --help

---

Running SSRLeakGuard

Phase 1 — SSR Data Exposure

	ssrleakguard http://localhost:3000/leak1

Detects sensitive data embedded in SSR output.

---

Phase 2 — Authorization Inconsistency

	ssrleakguard http://localhost:3000/leak2 \
	  --context guest \
	  --context user:next-auth.session-token=abc123

Compares SSR responses across different authorization contexts.

---

Test Pages


The following intentionally vulnerable pages can be used to evaluate each phase.


leak1.js — Phase 1 Test

Demonstrates over‑fetching and serialization of sensitive data into SSR output.

All users receive the same SSR response, but sensitive fields are unnecessarily exposed.

---

leak2.js — Phase 2 Test

Demonstrates authorization‑dependent SSR output.

Authenticated users receive additional SSR data, allowing SSRLeakGuard to detect inconsistencies across contexts.

---

Output Overview

- Phase 1 provides detailed, forensic‑style findings with context and evidence.

- Phase 2 reports clean, field‑level authorization differences across users.

---

Detection Capabilities

SSRLeakGuard can automatically detect 14 types of sensitive data:

Critical Severity

AWS Access Keys
AWS Secret Keys
GitHub Personal Access Tokens
Private Keys (RSA/SSH)

High Severity

JSON Web Tokens (JWT)
Generic API Keys
Bearer Tokens
Slack Tokens
Database Connection Strings
Session IDs

Medium Severity

Email Addresses
Phone Numbers

---

ssrleakguard/
├── ssrleakguard/
│   ├── core/
│   │   ├── analyzer.py      # Main analysis logic
│   │   ├── context.py       # Authorization context handling
│   │   ├── differ.py        # SSR state comparison
│   │   └── http_client.py   # HTTP request handling
│   ├── detectors/
│   │   ├── ssr_detector.py  # SSR framework detection
│   │   ├── nextjs_parser.py # Next.js data extraction
│   │   └── secret_scanner.py # Secret pattern matching
│   ├── utils/
│   │   ├── patterns.py      # Secret detection patterns
│   │   ├── normalizer.py    # Data normalization
│   │   └── reporter.py      # Output formatting
│   └── cli.py               # Command-line interface
├── README.md
├── requirements.txt
└── setup.py