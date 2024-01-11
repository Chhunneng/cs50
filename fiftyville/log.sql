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
-- Step 4: Find the names associated with the account numbers from the suspect list.
SELECT name, atm_transactions.account_number, amount
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2023 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw';
--We now have a list of individuals associated with the ATM transactions on Leggett Street. Bruce seems to be a common name across multiple sources of information. Let's continue building our suspect list and exploring other clues.
-- Step 5: Continue the investigation with Raymond's clues about the flight.
-- Find the flights on July 29 from Fiftyville airport, ordering them by time.
SELECT flights.id, full_name, city, flights.hour, flights.minute
FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29
ORDER BY flights.hour, flights.minute;
