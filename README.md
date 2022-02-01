## This repository contains code that gets data regarding financial disclosures from the [Court Listener](https://www.courtlistener.com/) [API](https://www.courtlistener.com/api/rest-info/)

* [main.py]('/main.py'): contains driver code that interacts with all the other files. Only file that should be run. When run it will grab all the data and populate output.csv with it
* [auth_token.py](/auth_token.py): Reads API authentication token.
* [AUTH_TOKEN.txt](/AUTH_TOKEN.txt): Contains API authentication token. Obtain yours from [here](https://www.courtlistener.com/api/rest-info/) and paste it into this file
* [fields.py](/fields.py): contains the code that grabs all the fields from every disclosure
* [lookups.py](/lookups.py): contains some extra lookup tables (aside form the ones embedded in [fields.py](/fields.py)) for the values returned from the API 
* [utils.py](/utils.py): contains some utility functions
* [requirements.txt]('/requirements.txt'): contains the list of dependencies used. Install them by running `pip install -r requirements.txt`
* [README.txt]('/readme.txt'): readme in txt format

## Overview
Every year judges file a financial disclosure form as mandated by law. Courtlistener parses these forms which are PDFs into their database. Here is an example of one of the unederlying forms that will help me explain what every row in our data is: https://storage.courtlistener.com/us/federal/judicial/financial-disclosures/9529/patricia-a-sullivan-disclosure.2019.pdf
Disclosures are seperated into certain categories, such as positions, or investments. Each individual listing under a certain type of disclosure, is a row in our data. So if you look at that PDF, Member and Officer at Board of Directors of Roger Williams University School of Law, would be the basis for one row. If you scroll down to investments, MFS Investment Management (Educational Funds) (H), would also be the basis for one row. For that row, the fields listed below under Disclosure Fields -> Investments will all be filled out (unless they are not present in the courtlistner database). The Common Fields and Person Fields will also be filled out. Person fields are fields unique to the judge, and common fields unique to the report. So for the two example rows, the common fields and person fields would remain constant (as the judge and report are the same), but the disclosure fields will be different. For the first one, the fields under Disclosure Fields -> Positions will be filled out, with the rest of the disclosure fields empty, and for the second one the fields under Disclosure Fields -> Investments would be filled out.





## Common Fields



sha1: SHA1 hash of the generated PDF
is_amended: Is disclosure amended?
Disclosure PDF: PDF of the original filed disclosure
Year Disclosed: Date of judicial agreement.
report_type: Financial Disclosure report type
addendum_redacted: Is the addendum partially or completely redacted?
Disclosure Type: Type of the disclosure, (investments, debts, etc)

## Disclosure Fields


Note: Depending on the Disclosure Type field above, the corresponding fields will be filled in for the row

agreements:
        date_raw: Date of judicial agreement.
        parties_and_terms: Parties and terms of agreement (ex. Board Member NY Ballet)
        redacted: Does the agreement row contain redaction(s)?
        financial_disclosure: The financial disclosure associated with this agreement.
        id: ID of the record.
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

debts:
        creditor_name: Liability/Debt creditor
        description: Description of the debt
        value_code: Form code for the value of the judicial debt, substituted with the numerical values of the range.
        value_code_max: The maximum value of the value_code.
        redacted: Does the debt row contain redaction(s)?
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

gifts:
        source: Source of the judicial gift. (ex. Alta Ski Area).
        description: Description of the gift (ex. Season Pass).
        value: Value of the judicial gift, (ex. $1,199.00)
        redacted: Does the gift row contain redaction(s)?
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

investments:
        page_number: The page number the investment is listed on.  This is used to generate links directly to the PDF page.
        description: Name of investment (ex. APPL common stock).
        redacted: Does the investment row contains redaction(s)?
        income_during_reporting_period_code: Increase in investment value - as a form code. Substituted with the numerical values of the range.
        income_during_reporting_period_code_max: Maximum value of income_during_reporting_period_code.
        income_during_reporting_period_type: Type of investment (ex. Rent, Dividend). Typically standardized but not universally.
        gross_value_code: Investment total value code at end of reporting period as code (ex. J (1-15,000)). Substituted with the numerical values of the range.
        gross_value_code_max: Maximum value of the gross_value_code.
        gross_value_method: Investment valuation method code (ex. Q = Appraisal)
        transaction_during_reporting_period: Transaction of investment during reporting period (ex. Buy, Sold)
        transaction_date_raw: Date of the transaction, if any (D2)
        transaction_date: Date of the transaction, if any (D2)
        transaction_value_code: Transaction value amount, as form code (ex. J (1-15,000)). Substituted with the numerical values of the range.
        transaction_value_code_max: Maximum value of transaction_value_code.
        transaction_gain_code: Gain from investment transaction if any (ex. A (1-1000)). Substituted with the numerical values of the range.
        transaction_gain_code_max: Maximum value of transaction_gain_code.
        transaction_partner: Identity of the transaction partner
        has_inferred_values: If the investment name was inferred during extraction. This is common because transactions usually list the first purchase of a stock and leave the name value blank for subsequent purchases or sales.
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

non_investment_incomes:
        date_raw: Date of non-investment income (ex. 2011).
        source_type: Source and type of non-investment income for the judge (ex. Teaching a class at U. Miami).
        income_amount: Amount earned by judge, often a number, but sometimes with explanatory text (e.g. 'Income at firm: $xyz').
        redacted: Does the non-investment income row contain redaction(s)?
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

positions:
        non judiciary position: Position title (ex. Trustee).
        organization_name: Name of organization or entity (ex. Trust #1).
        redacted: Does the position row contain redaction(s)?
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown

reimbursements:
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown
        source: Source of the reimbursement (ex. FSU Law School).
        date_raw: Dates as a text string for the date of reimbursements. This is often conference dates (ex. June 2-6, 2011). 
        location: Location of the reimbursement (ex. Harvard Law School, Cambridge, MA).
        purpose: Purpose of the reimbursement (ex. Baseball announcer).
        items_paid_or_provided: Items reimbursed (ex. Room, Airfare).
        redacted: Does the reimbursement contain redaction(s)?

spouse_incomes:
        id: ID of the record
        date_created: The moment when the item was created.
        date_modified: The last moment when the item was modified. A value in year 1750 indicates the value is unknown
        source_type: Source and type of income of judicial spouse (ex. Salary from Bank job).
        redacted: Does the spousal-income row contain redaction(s)?
        date_raw: Date of spousal income (ex. 2011).



## Person Fields

fjc_id: The ID of a judge as assigned by the Federal Judicial Center.
Date of Birth: The date of birth for the person
name_last: The last name of this person
political_affiliations: Political affiliations for the judge. Variable length so combined by a comma
Death Country: The country where the person died.
Birth City: The city where the person was born.
name_suffix: Any suffixes that this person's name may have
aba_ratings: American Bar Association Ratings. Variable length so combined by a comma
name_first: The first name of this person.
Death State: The state where the person died.
sources: Sources about the person. Variable length so combined with a newline
Birth Country: The country where the person was born.
cl_id: A unique identifier for judge, also indicating source of data.
gender: The person's gender
name_middle: The middle name or names of this person
ftm_eid: The ID of a judge as assigned by the Follow the Money database.
Death City: The city where the person died.
positions: Positions of person. Variable length so combined with a newline
ftm_total_received: The amount of money received by this person and logged by Follow the Money.
Date of Death: The date of death for the person
religion: The religion of a person
educations: Educations of the person. Variable length so combined by a comma
bachelor school: Name of the school from which they got their Bachelor's degree, and/or Bachelor's of Law degree. Variable length so combined by a comma
juris doctor school: name of the school from which they got their jusris doctor degree. their Bachelor's degree, and/or Bachelor's of Law degree. Variable length so combined by a comma
race: Race of the person. Variable length so combined by a comma
Birth State: The state where the person was born.


