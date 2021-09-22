-- Keep a log of any SQL queries you execute as you solve the mystery.
-- .schema 
-- .tables 
-- .schema courthouse_security_logs
-- SELECT id, hour, minute, activity, license_plate  FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 order BY hour, minute
/* SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street = 'Chamberlin Street' */
--  Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.
/* SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28  */
/* SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND activity = 'exit' */
/* SELECT * FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND transaction_type ='withdraw' AND atm_location = 'Fifer Street' */
/* SELECT * FROM phone_calls  
JOIN people ON phone_number = caller
JOIN bank_accounts ON person_id = people.id 
WHERE year = 2020 AND month = 7 AND day = 28 ORDER BY duration; */
/* SELECT * FROM flights 
JOIN passengers ON flights.id = passengers.flight_id
JOIN people ON passengers.passport_number = people.passport_number
JOIN bank_accounts ON bank_accounts.person_id = people.id
/* JOIN atm_transactions ON atm_location.account_number = bank_accounts.account_number  
WHERE year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute */
    /* SELECT account_number FROM bank_accounts */
/* 
SELECT * FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON people.id = bank_accounts.person_id
JOIN courthouse_security_logs on courthouse_security_logs.license_plate = people.license_plate
JOIN phone_calls ON phone_calls.caller = people.phone_number
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON airports.id = flights.destination_airport_id
--JOIN airports ON airports.id = flights.origin_airport_id
WHERE atm_transactions.year = 2020 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.transaction_type ='withdraw' AND atm_transactions.atm_location = 'Fifer Street'
AND flights.day = 29 AND flights.year = 2020 AND flights.month = 7 AND phone_calls.day = 28
*/


SELECT * FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON people.id = bank_accounts.person_id
JOIN courthouse_security_logs on courthouse_security_logs.license_plate = people.license_plate
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON airports.id = flights.destination_airport_id
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE atm_transactions.year = 2020 AND atm_transactions.month = 7 AND atm_transactions.day = 28 AND atm_transactions.transaction_type ='withdraw' AND atm_transactions.atm_location = 'Fifer Street'
AND courthouse_security_logs.activity = 'exit' AND flights.origin_airport_id = 8 AND flights.day = 29 AND flights.year = 2020 AND flights.month = 7
AND phone_calls.day = 28 AND phone_calls.month = 7 AND phone_calls.year = 2020 ORDER BY flights.hour, flights.minute 


/* SELECT * FROM people WHERE phone_number = '(704) 555-5790' */
/* (375) 555-8161	
(704) 555-5790	 */
