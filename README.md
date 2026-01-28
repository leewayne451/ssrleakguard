SSRLeakGuard is a security testing tool for detecting server-side rendering (SSR) data exposure and authorization inconsistencies in modern web applications, with a focus on Next.js.

It is designed as a phased research tool:

- Phase 1: SSR data exposure detection

- Phase 2: Authorization inconsistency detection via differential SSR analysis

---

Table of Contents

1. Requirements

2. Setting up SSRLeakGuard (Python virtual environment)

3. Installing dependencies

4. Running SSRLeakGuard

5. Creating test SSR leaks

- leak1.js (Phase 1)
- leak2.js (Phase 2)

6. Expected behavior

---

1. Requirements

System requirements

- Python 3.8+

- Node.js 18+

- npm (bundled with Node.js)

Supported SSR framework

- Next.js (Pages Router)

---

2. Setting up SSRLeakGuard (Python venv)

From the root of the SSRLeakGuard repository:

Create a virtual environment
	python -m venv venv

Activate the virtual environment
Windows (PowerShell):
	venv\Scripts\activate

Windows (Command Prompt):
	venv\Scripts\activate.bat

macOS / Linux:
	source venv/bin/activate

You should now see:
	(venv)

in your terminal.

---

3. Installing dependencies

Install required Python packages
	pip install -r requirements.txt

Install SSRLeakGuard in editable mode
	pip install -e .

Verify installation
	ssrleakguard --help

---

4. Running SSRLeakGuard

Phase 1 — SSR data exposure detection
	ssrleakguard http://localhost:3000/leak1

Phase 2 — Authorization inconsistency detection
	ssrleakguard http://localhost:3000/leak2 \
	  --context guest \
	  --context user:next-auth.session-token=abc123

---

5. Creating test SSR leaks (Next.js)

Install node.js with Windows LTS installer, make sure to select Add to PATH (https://nodejs.org)
	npx create-next-app vulnerable-nextjs
	cd vulnerable-nextjs
	npm run dev

All test files go in:
	vulnerable-nextjs/pages/

---

5.1 leak1.js — Phase 1 test (SSR data exposure)

This file demonstrates over-fetching and serialization of sensitive data into SSR output.

Create:
	pages/leak1.js

	export async function getServerSideProps() {
	  const userRecord = {
	    id: "u_83921",
	    username: "john_doe",
	    email: "john@example.com", // PII
	    role: "admin",             // authorization detail
	    internalId: "INT-77431",    // internal identifier
	  };
	
	  return {
	    props: {
	      user: userRecord,
	    },
	  };
	}
	
	export default function Leak1Page({ user }) {
	  return (
	    <div>
	      <h1>User Profile</h1>
	      <p>
	        <strong>Username:</strong> {user.username}
	      </p>
	    </div>
	  );
	}

---

5.2 leak2.js — Phase 2 test (authorization inconsistency)

This file demonstrates SSR output changing based on authentication context.

Create:
	pages/leak2.js

	export async function getServerSideProps(context) {
	  const cookies = context.req.headers.cookie || "";
	  const isAuthenticated = cookies.includes("next-auth.session-token");
	
	  const baseUser = {
	    username: "john_doe",
	    email: "john@example.com", // exposed to all users
	  };
	
	  if (!isAuthenticated) {
	    return {
	      props: {
	        user: baseUser,
	      },
	    };
	  }
	
	  return {
	    props: {
	      user: {
	        ...baseUser,
	        role: "admin",          // only for authenticated users
	        internalId: "INT-49321", // only for authenticated users
	      },
	    },
	  };
	}
	
	export default function Leak2Page({ user }) {
	  return (
	    <div>
	      <h1>Welcome</h1>
	      <p>
	        <strong>Username:</strong> {user.username}
	      </p>
	      <p>
	        <strong>Email:</strong> {user.email}
	      </p>
	    </div>
	  );
	}

---

6. Expected behavior

Phase 1 (leak1.js)

- Email, role, and internal ID detected in SSR output

- Findings reported with detailed context and snippets

Phase 2 (leak2.js)

- Guest vs authenticated SSR output differs

---

Summary


SSRLeakGuard demonstrates how server-side rendering can introduce subtle but serious security risks, even when APIs and authentication mechanisms are correctly implemented.

The included test cases provide:

- Clear Phase 1 validation

- Clear Phase 2 validation

- Reproducible experimental results