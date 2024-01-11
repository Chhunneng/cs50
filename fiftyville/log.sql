-- Step 1: Find the crime scene report for the theft on Humphrey Street on July 28, 2023.
SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street' AND year = 2023 AND month = 7 AND day = 28;

-- Step 2: Find the names and transcripts of witnesses from the interviews table.
SELECT name, transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;

-- Next, we'll focus on Eugene's statement, as he mentioned seeing the thief at the ATM on Leggett Street. We want to identify the account number of the person who made a withdrawal at that ATM around the time of the theft.
-- Step 3: Find the account number and withdrawal amount from the ATM transactions on Leggett Street.
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
--Now, let's proceed to find the names of the individuals linked to these account numbers. We'll include this information in our suspect list.
