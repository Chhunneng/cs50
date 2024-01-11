-- Query 1: Examine the crime scene reports for the date and location of the theft
SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street' AND year = 2023 AND month = 7 AND day = 28;

-- Query 2: Once you find the crime scene report, investigate further details
SELECT description
FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND year = 2023 AND street = 'Humphrey Street';

-- Query 3: Explore interviews related to the crime
SELECT *
FROM interviews
WHERE day = 28 AND month = 7 AND year = 2023;

-- Query 4: Continue to gather information about the suspect(s)
SELECT *
FROM people
WHERE name = 'SuspectName';

-- Query 5: Check the bakery security logs for suspicious activity
SELECT *
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2023 AND activity = 'Theft';

-- Query 6: Investigate ATM transactions on the same date
SELECT *
FROM atm_transactions
WHERE day = 28 AND month = 7 AND year = 2023;

-- Query 7: Look for flights on the date of the theft
SELECT *
FROM flights
WHERE day = 28 AND month = 7 AND year = 2023;

-- Query 8: Explore passengers on relevant flights
SELECT *
FROM passengers
WHERE flight_id = FlightID;

-- Query 9: Check airport information for the destination city
SELECT *
FROM airports
WHERE city = 'DestinationCity';

-- Query 10: Identify the person who helped the thief escape
SELECT *
FROM people
WHERE name = 'AccompliceName';
