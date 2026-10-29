## 1. Contradicting minimum-amount error messages

**Steps:** POST /v1/orders with amount = -1, then amount = 0
**Expected:** a consistent message that states the actual minimum (100 paise)
**Actual:**
- amount = -1 → "amount: must be no less than 0."
- amount = 0  → "Order amount less than minimum amount allowed"
**Impact:** the first message implies 0 is valid; neither tells the caller the real minimum.
**Test:** `test_create_order_with_invalid_input[negative]`, `[zero]`