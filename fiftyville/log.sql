-- Investigating the crime scene report to find information about the theft
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Identifying the witnesses from interviews on the same day
SELECT name, transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;

-- Checking ATM transactions near the crime scene
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Finding names associated with account numbers for potential suspects
SELECT name, atm_transactions.amount
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2023 AND atm_transactions.month = 7 AND atm_transactions.day = 28
  AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw';

-- Checking flights from Fiftyville airport on the following day
SELECT flights.id, full_name, city, hour, minute
FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
  AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29
ORDER BY flights.hour, flights.minute;

-- Listing passengers on the identified flight
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.year = 2023 AND flights.month = 7 AND flights.day = 29 AND flights.hour = 8 AND flights.minute = 20
ORDER BY passengers.passport_number;

-- Checking phone call records to find the person who bought the tickets
SELECT name, phone_calls.duration
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2023 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;

-- Identifying the person who drove away from the bakery
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.year = 2023 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28
  AND bakery_security_logs.activity = 'exit' AND bakery_security_logs.hour = 10
  AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25
ORDER BY bakery_security_logs.minute;

-- Checking Bruce's Phone number
SELECT phone_number
FROM people
WHERE name = 'Bruce';

-- Checking phone call records for the accomplice
SELECT id, year, month, day, duration, caller, receiver
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28
  AND (caller = '(367) 555-5533' OR receiver = '(367) 555-5533');

-- Identifying the accomplice's name
SELECT name
FROM people
WHERE phone_number = '(375) 555-8161';
