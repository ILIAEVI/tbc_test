# Bug Identification


## Task_2

# `calculate_payments` Function

## Overview

The `calculate_payments` function processes a list of applicants, where each applicant includes a currency and a list of payments. It calculates the total payment per currency, applying business logic only to active payments. This version includes several important validations and bug fixes over the original implementation.

---

## ✅ Fixed Issues and Improvements Over Initial Version

### 1. Input Type Validation
- **Bug:** Original code accepted any type for `applicants`, risking runtime errors.
- **Fix:** Raises a `TypeError` if `applicants` is not a list.

### 2. Currency Validation
- **Bug:** Currency defaulted to `"GEL"` without validating presence or correctness.
- **Fix:** 
  - Validates that currency is a non-empty string.
  - Applies `.strip().upper()` for consistency.
  - Raises `ValueError` if invalid.

### 3. Payments List Validation
- **Bug:** No checks for `payments` field.
- **Fix:** 
  - Validates that `payments` is a list.
  - Raises `ValueError` if the list is empty.

### 4. Payment Item Type Validation
- **Bug:** Assumed each payment is a dictionary.
- **Fix:** Verifies each payment is a `dict`; raises `TypeError` otherwise.

### 5. Active Flag Validation
- **Bug:** No validation on the type of `active`.
- **Fix:** Ensures `active` is a boolean value.

### 6. Business Logic Preservation
- **Fix:** Preserved the business logic line `if pay.get("active", True)` so only active payments are considered.

### 7. Field Presence and Type Validation
- **Bug:** No checks for required fields or zero division risk.
- **Fixes:**
  - Checks for presence of `'base'`, `'incomeshare'`, and `'amount'`.
  - Ensures `base` is not zero (avoids division by zero).
  - Validates all numeric fields using `float()`.
  - Raises exceptions on invalid or missing data.

### 8. Exception Handling and Messaging
- **Improvement:** Clear and informative error messages for each type of issue, aiding debugging and maintenance.

---