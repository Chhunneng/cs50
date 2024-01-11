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
--It seems the earliest flight on July 29 is to LaGuardia Airport in New York City (Flight ID 36). This aligns with Raymond's information about the thief planning to take the earliest flight out of Fiftyville.
-- Step 6: Identify passengers on the flight to New York City.
-- Checking the list of passengers on the identified flight. Putting them all in 'Suspect List'.
-- Order the names according to their passport numbers.
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36
ORDER BY passengers.passport_number;
--Now, let's move on to the next step. Raymond mentioned that the thief called someone and talked for less than a minute, asking them to buy a flight ticket for the earliest flight on July 29, 2021. We need to check the phone call records to identify the person who bought the tickets.
-- Step 7: Identify the person who bought the flight tickets.
-- Checking the possible names of the caller, and putting these names in the 'Suspect List'.
-- Order them according to the durations of the calls.
SELECT name, phone_calls.duration
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2023
  AND phone_calls.month = 7
  AND phone_calls.day = 28
  AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;

