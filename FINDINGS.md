# Findings – Razorpay Orders API (Test Mode)

Observations from running this test suite against Razorpay's Orders API in test mode.
Each entry records what was sent, what I expected, what actually came back, and why it matters
to someone integrating with the API.

These are behaviours worth knowing, **not** necessarily bugs. Some are design choices.
Where a claim still needs more evidence, it is marked as an open question.

**Environment:** `https://api.razorpay.com/v1`, test-mode keys, Basic Auth, October 2026.

## Summary

| # | Finding | Area | Severity |
|---|---|---|---|
| 1 | Contradicting minimum-amount error messages | Validation | Medium |
| 2 | Type validation runs before range validation | Validation | Low |
| 3 | Malformed order ID returns 400 (404 behaviour still to verify) | Fetch | Open question |
| 4 | Error message drops the `order_` prefix from the ID | Fetch | Low |
| 5 | Optional error fields use the string `"NA"` instead of `null` | Error format | Medium |
| 6 | Authentication failure (401) uses error code `BAD_REQUEST_ERROR` | Auth | Medium |
| 7 | Empty and missing credentials return different messages | Auth | Low |
| 8 | USD order creation depends on account configuration | Test portability | Info |

---

## 1. Contradicting minimum-amount error messages

**Steps:** `POST /v1/orders` with `amount = -1`, then with `amount = 0` and `amount = 1` (currency `INR`)

**Expected:** one consistent message that states the actual minimum (100 paise = ₹1)

**Actual:**
- `amount = -1` → 400, `"amount: must be no less than 0."`
- `amount = 0` → 400, `"Order amount less than minimum amount allowed"`
- `amount = 1` → 400, `"Order amount less than minimum amount allowed"`

**Impact:** the first message implies that 0 is a valid amount, but 0 is then rejected by a
second check. Neither message tells the caller what the minimum actually is. There appear to be
two separate validation layers (a field-level check and a business-rule check) with different wording.

**Test:** `test_create_order_with_invalid_input` (cases `-1`, `0`, `1`)

---

## 2. Type validation runs before range validation

**Steps:** `POST /v1/orders` with `amount = -599.99`, currency `INR`

**Expected:** both problems reported, or the more fundamental one (negative amount)

**Actual:** 400, `"The amount must be an integer."` Only the type error is returned, and the
negative value isn't mentioned.

**Impact:** errors are reported one at a time. A client that fixes only the reported problem
(e.g. rounds to `-600`) hits a second error on the next request.

**Test:** `test_create_order_with_invalid_input` (case `-599.99`)

---

## 3. Malformed order ID returns 400 – 404 behaviour still to verify

**Steps:** `GET /v1/orders/order_doesnotexist123`

**Actual:** 400, `"doesnotexist123 is not a valid id"`

**Analysis:** this ID is *malformed*. Real order IDs have 14 alphanumeric characters after
`order_`. So a 400 is defensible here: it's input validation, not "not found".

**Open question:** what does a **well-formed** but non-existent ID return
(e.g. `order_ABCDEFGHIJ1234`)? REST convention would be `404 Not Found`. If it also returns
400, that's a deviation worth documenting. *Test to be added.*

**Test:** `test_fetch_non_existant_order`

---

## 4. Error message drops the `order_` prefix from the ID

**Steps:** same request as #3

**Expected:** the message quotes the ID exactly as sent: `"order_doesnotexist123 is not a valid id"`

**Actual:** `"doesnotexist123 is not a valid id"`

**Impact:** minor, but when debugging from logs, searching for the ID that was sent won't
match this error message.

**Test:** `test_fetch_non_existant_order`

---

## 5. Optional error fields use the string `"NA"` instead of `null`

**Steps:** `POST /v1/orders` with `amount = 0`, currency `INR`

**Actual:**
```json
{
  "error": {
    "code": "BAD_REQUEST_ERROR",
    "description": "Order amount less than minimum amount allowed",
    "metadata": {},
    "reason": "NA",
    "source": "order",
    "step": "NA"
  }
}
```
Compare with the unknown-field error, where the same fields carry real values:
`"reason": "extra_field_sent"`, `"source": "business"`, `"step": "payment_initiation"`.

**Impact:** a client can't use a simple `null` check to decide whether `reason` or `step`
is present. It has to know that the string `"NA"` means "no value". In this suite's pydantic
schema, these fields are typed as `str` rather than `Optional[str]` for that reason.

**Test:** `test_create_order_with_invalid_input`, `test_create_order_with_unknown_field`

---

## 6. Authentication failure (401) uses error code `BAD_REQUEST_ERROR`

**Steps:** `POST /v1/orders` with an invalid key ID / key secret

**Actual:** HTTP **401**, body:
```json
{"error": {"code": "BAD_REQUEST_ERROR", "description": "Authentication failed"}}
```

**Expected:** an authentication-specific error code consistent with the 401 status

**Impact:** clients that branch on `error.code` alone can't tell an auth failure from a
validation failure. They must also check the HTTP status code.

**Test:** `test_wrong_auth`

---

## 7. Empty and missing credentials return different messages

**Steps:**
- (a) Basic Auth with an empty key ID and empty secret
- (b) no `Authorization` header at all

**Actual:**
- (a) 401, `"Authentication failed"`
- (b) 401, `"Please provide your api key for authentication purposes"`

**Impact:** low, but inconsistent. An empty key is effectively "no key", yet only (b) tells the
developer what to do. Someone whose key failed to load from config (an empty environment variable)
gets the less helpful message.

**Note:** this suite ran into exactly that situation in CI, where a misnamed secret produced an
empty key and every request failed with `"Authentication failed"`.

**Tests:** `test_wrong_auth` (empty credentials case), `test_empty_auth`

---

## 8. USD order creation depends on account configuration

**Steps:** `POST /v1/orders` with `amount = 1000`, currency `USD`

**Actual (on my test account):** 200, order created

**Impact on testing:** whether non-INR orders are accepted depends on whether international
payments are enabled on the account. This test passes on my account but may fail on another,
so it isn't portable.

**Decision:** kept in the suite and documented here as account-dependent.

**Test:** `test_create_order_with_valid_amounts` (case `1000-USD`)