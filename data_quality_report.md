# Mobile-Money Agent Data Quality Report

## 1. Introduction
This report summarises the data-quality assessment and cleaning of mobile-money transaction records. The original dataset contained 612 records and was assessed before cleaning.

## 2. Data Quality Issues Identified

The audit examined the following dimensions:

- **Uniqueness:** Duplicate transaction IDs were identified and removed.
- **Completeness:** Missing transaction amounts were identified and imputed using the median.
- **Consistency:** Transaction types were standardised to Deposit and Withdrawal.
- **Validity:** Transaction amounts were converted to numeric values and transaction dates were standardised.
- **Accuracy:** Potential outliers were identified using the Interquartile Range (IQR) method and flagged for review.
- **Referential integrity:** Transactions containing agent IDs absent from the agent register were identified.

## 3. Cleaning Actions

Duplicate records were removed while retaining the first occurrence. Missing and invalid amounts were converted to numeric values and imputed using the median. Transaction types were standardised, dates were converted to datetime format, and potential outliers were flagged rather than automatically deleted.

The transaction records were also merged with the agent register to attach county information. Unmatched agent records were retained and labelled Unknown.

## 4. Validation Results

The final cleaned dataset contained 600 transactions.

| Validation measure | Result |
|---|---:|
| Remaining duplicate IDs | 0 |
| Missing amounts | 0 |
| Missing dates | 0 |
| Unknown agents | 7 |
| Flagged outliers | 53 |
| Imputed amounts | 20 |

## 5. Privacy Considerations

The handling of transaction records should comply with the Kenya Data Protection Act, 2019. Access should be restricted, personal identifiers protected, and reporting should use aggregated information wherever possible.

## 6. Conclusion and Recommendations

The cleaning process improved the consistency, completeness, validity and uniqueness of the transaction dataset. The remaining seven unmatched agent records should be investigated against the agent register. The 53 flagged outliers should also be reviewed before financial decisions are made. Regular data validation and maintenance of accurate agent records are recommended.
