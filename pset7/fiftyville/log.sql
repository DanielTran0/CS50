-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find out what happened on that day and street (id for easy reference)
SELECT id, description FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28 AND street = "Chamberlin Street";

-- See who the witnesses are and what they have to say
SELECT id, name, transcript FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;

-- Find the car the thief took at the courthouse (ruth statement)
SELECT id, minute, license_plate, activity FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit";

-- Match license plate to people (SUSPECTS)
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit");

-- See atm transactions before crime (eugene statement)
SELECT id, account_number, amount FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw";

-- Match transactions to bank account
SELECT account_number, person_id FROM bank_accounts
WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw");

-- Match bank account to people (SUSPECTS)
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE id in 
(SELECT person_id FROM bank_accounts
WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"));

-- See phonecalls (raymond statement)
SELECT id, caller, receiver, duration FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;

-- Match caller to person (SUSPECTS)
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE phone_number IN  
(SELECT caller FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60);

-- Compare the 3 suspect lists (SUSPECTS)
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE phone_number IN  
(SELECT caller FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60)
INTERSECT
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE id in 
(SELECT person_id FROM bank_accounts
WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"))
INTERSECT
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit");
-- SUSPECTS that are on all 3 lists are russell and ernest

-- Find airports in Fiftyville (id 8, Fiftyville Regional Airport)
SELECT id, abbreviation, full_name FROM airports
WHERE city = "Fiftyville";

-- Look at flights at that airport leaving the next day (day 29)
SELECT id, destination_airport_id, hour, minute FROM flights
WHERE origin_airport_id = 8 AND year = 2020 AND month = 7 AND day = 29 ORDER BY hour;

-- Look at passengers on the earliest flight (id 36, 8am)
SELECT passport_number, seat FROM passengers
WHERE flight_id = 36;

-- Match passengers to people
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE passport_number IN 
(SELECT passport_number FROM passengers
WHERE flight_id = 36);

-- Match passengers to suspect list
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE passport_number IN 
(SELECT passport_number FROM passengers
WHERE flight_id = 36)
INTERSECT
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE phone_number IN  
(SELECT caller FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60)
INTERSECT
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE id in 
(SELECT person_id FROM bank_accounts
WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street" AND transaction_type = "withdraw"))
INTERSECT
SELECT id, name, license_plate, phone_number, passport_number FROM people
WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit");
-- THIEF IS ERNEST

-- See where he went (london)
SELECT city FROM airports
WHERE id = 
(SELECT destination_airport_id FROM flights
WHERE origin_airport_id = 8 AND year = 2020 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20);

-- See who is the accomplice is by the finding the person Ernest called (Jonathan)
SELECT receiver FROM phone_calls
WHERE caller = 
(SELECT phone_number FROM people
WHERE name = "Ernest") 
AND year = 2020 AND month = 7 AND day = 28 AND duration <= 60;
-- number is (375) 555-8161

-- Find the person behind the number (Berthold)
SELECT name FROM people
WHERE phone_number = "(375) 555-8161";