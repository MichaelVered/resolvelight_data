# Supplier Name Differences Summary

This document summarizes the differences between the original invoice files and their '_' prefixed replicas. The '_' prefixed files contain supplier names with misleading similarity - they appear similar at first glance but represent clearly different companies.

## Summary Table

| Modified Supplier Name (in '_' file) | Contract Supplier Name (Golden) |
|--------------------------------------|----------------------------------|
| Cosmic Apps Company | Quantum Apps Co. |
| CodeForge Solutions Inc. | CodeCraft Labs LLC |
| Stellar Technologies Inc. | Starlight Engineering |
| BrightData Systems LLC | BrightByte Technologies |
| NovaTech Systems Inc. | NovaSoft Solutions Ltd. |
| VectorTech Solutions Group | VectorWorks Group |
| NexusTech Solutions LLC | Nexus Innovations LLC |
| SkylineTech Digital Solutions | Skyline Digital Partners |
| PixelTech Solutions Inc. | Pixel Perfect Devs Inc. |
| CatalystTech Solutions Collective | Catalyst Dev Collective |

## Notes

- All other fields remain identical between original and '_' prefixed files
- Vendor IDs are unchanged (same vendor_id in both versions)
- The changes create distinct but slightly similar company names - clearly different companies but with enough similarity to potentially confuse automated systems or inattentive reviewers
- These variations demonstrate how strict validation systems might reject invoices due to exact name mismatches, even when the names share similar words or structure
- The modified names represent completely different legal entities, not just variations of the same company

## Validation Impact

These supplier name variations would likely be:
- **Rejected by strict validation**: Exact string matching would fail
- **Potentially approved by human reviewers**: If the reviewer doesn't carefully compare against the contract/PO, the similarity might be overlooked
- **Clear fraud indicators**: If intentionally used, these represent attempts to impersonate legitimate suppliers

