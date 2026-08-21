# Better Auth recipe

Better Auth is active because this project requires identity. Signup remains disabled in the running app; only the idempotent local seed enables account creation.

Protected reads and every mutation must call `requireSession()` on the server. Never rely only on hiding client UI.
