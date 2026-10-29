# Razorpay Orders API – Test Automation Framework

![API Tests](https://github.com/<username>/<repo>/actions/workflows/api-tests.yml/badge.svg)

Automated API test suite for Razorpay's Orders API (test mode), built with
pytest, requests and pydantic, and run on every push via GitHub Actions.

## What's tested
| Area | Cases |
|---|---|
| Create order – valid | min amount (100), normal, large, INR/USD |
| Create order – invalid | decimal, negative, zero, below minimum, invalid currency, missing fields, unknown field |
| Fetch order | by id, non-existent id |
| Auth | no auth, wrong key, wrong secret, empty credentials |
| Contract | every response validated against pydantic schemas |

## Key findings
Short summary + link to FINDINGS.md (2–3 most interesting ones)

## Project structure
api/        → HTTP client and pydantic schemas
configs/    → environment config
tests/      → test files by feature
conftest.py → shared fixtures

## How to run
1. Clone, create venv, `pip install -r requirements.txt`
2. Create `.env` with `key_id` and `key_secret` (Razorpay test-mode keys)
3. `pytest -v`

## CI
What runs, when, where the report is, how secrets are handled