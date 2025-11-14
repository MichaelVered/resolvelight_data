# 15 Realistic Permissible Errors That Strict Validation Would Reject

These are errors that an expert human reviewer would approve (understanding context, business relationships, and common practices), but strict automated validation systems like ResolveLight would REJECT.

## 1. **Minor Date Format Variations**
- **Error**: Invoice `issue_date` is "2025-02-20T00:00:00Z" (ISO 8601 with timestamp) vs PO expecting "2025-02-20" (date only)
- **Human Rationale**: Both represent the same date; timestamp is technically more precise
- **Strict Validation**: Rejects due to format mismatch

## 2. **Case Sensitivity in Supplier Names**
- **Error**: Invoice has "Quantum Apps Co." vs PO/Contract has "QUANTUM APPS CO." (all caps)
- **Human Rationale**: Same company, just different capitalization conventions
- **Strict Validation**: Rejects due to exact string mismatch

## 3. **Trailing Whitespace in Descriptions**
- **Error**: Line item description has "SSO and MFA foundation implementation " (trailing space) vs PO has "SSO and MFA foundation implementation"
- **Human Rationale**: Trivial formatting difference, content is identical
- **Strict Validation**: Rejects due to string comparison failure

## 4. **Numeric Precision Differences (Floating Point)**
- **Error**: Invoice `unit_price` is 150.0 (one decimal) vs PO has 150.00 (two decimals)
- **Human Rationale**: Mathematically equivalent, just different precision formatting
- **Strict Validation**: Rejects due to type/format mismatch in numeric comparison

## 5. **Abbreviated vs Full Company Names**
- **Error**: Invoice `bill_to_info.name` is "Global Innovations Corp." vs Contract has "Global Innovations Corporation"
- **Human Rationale**: "Corp." and "Corporation" are legally equivalent abbreviations
- **Strict Validation**: Rejects due to name mismatch

## 6. **Payment Terms with Minor Variations**
- **Error**: Invoice has "Net 30 days" vs PO has "Net 30"
- **Human Rationale**: Same payment terms, just more explicit wording
- **Strict Validation**: Rejects due to payment terms mismatch

## 7. **Invoice ID Format Variations**
- **Error**: Invoice has `invoice_id: "INV-AEG-2025-100"` but system expects format "INV-AEG-2025-001" (3-digit vs 3-digit with leading zeros)
- **Human Rationale**: Both are valid invoice identifiers, just different numbering schemes
- **Strict Validation**: Rejects due to format validation rules

## 8. **Currency Code Case Sensitivity**
- **Error**: Invoice has `currency: "usd"` (lowercase) vs PO has `currency: "USD"` (uppercase)
- **Human Rationale**: ISO currency codes are case-insensitive in practice
- **Strict Validation**: Rejects due to case-sensitive string comparison

## 9. **Optional Fields Present vs Absent**
- **Error**: Invoice includes `notes` field with discount explanation, but PO doesn't have a `notes` field
- **Human Rationale**: Additional information is helpful, not harmful
- **Strict Validation**: Rejects due to schema validation (unexpected field or field count mismatch)

## 10. **Rounding Differences in Totals**
- **Error**: Invoice `billing_amount` is 5600.0 (calculated with early payment discount) vs PO total is 6000.00, but discount is documented in notes
- **Human Rationale**: Discount is legitimate and documented, total is correct after discount
- **Strict Validation**: Rejects due to total amount mismatch with PO

## 11. **Vendor ID with/without Prefix**
- **Error**: Invoice has `vendor_id: "88301"` vs Contract has `vendor_id: "V-88301"`
- **Human Rationale**: Same vendor, just different ID formatting conventions
- **Strict Validation**: Rejects due to vendor ID mismatch

## 12. **Date Fields with Timezone Variations**
- **Error**: Invoice `due_date` is "2025-03-22" (local timezone implied) vs system expects "2025-03-22T23:59:59Z" (explicit UTC)
- **Human Rationale**: Same due date, timezone is irrelevant for date-only fields
- **Strict Validation**: Rejects due to date format/type mismatch

## 13. **Line Item Description with Minor Wording Changes**
- **Error**: Invoice description is "SSO and MFA foundation implementation" vs PO has "SSO & MFA foundation implementation" (ampersand vs "and")
- **Human Rationale**: Semantically identical, just different conjunction style
- **Strict Validation**: Rejects due to description text mismatch

## 14. **Missing Zero-Padding in Item IDs**
- **Error**: Invoice has `item_id: "AEG-1"` vs PO has `item_id: "AEG-001"`
- **Human Rationale**: Same item identifier, just different zero-padding convention
- **Strict Validation**: Rejects due to item ID format mismatch

## 15. **Tax Amount as Null vs Zero**
- **Error**: Invoice has `tax_amount: null` (field absent or null) vs PO/system expects `tax_amount: 0.00`
- **Human Rationale**: No tax is the same as zero tax; null is a valid representation
- **Strict Validation**: Rejects due to type mismatch (null vs number) or missing required field

---

## Common Themes

These errors typically fall into categories:
- **Format variations** (dates, numbers, strings)
- **Case sensitivity** (names, codes, IDs)
- **Whitespace/trimming** (descriptions, names)
- **Precision differences** (decimals, rounding)
- **Abbreviation variations** (Corp. vs Corporation)
- **Type representation** (null vs 0, string vs number)
- **Schema flexibility** (optional fields, additional metadata)

An expert human reviewer understands these are **semantic equivalences** and business context, while strict automated validation requires **exact matches** across all fields and formats.

