-- Step 1: Find the crime scene report for the theft on Humphrey Street on July 28, 2023.
SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street' AND year = 2023 AND month = 7 AND day = 28;

-- Step 2: Find the names and transcripts of witnesses from the interviews table.
SELECT name, transcript
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;
