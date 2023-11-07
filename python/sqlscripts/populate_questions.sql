-- 1. Autoshop question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'[Customers](Customer) bring their [cars](Car) to the shop for an estimate of repairs. 
One [mechanic](Mechanic) looks at the car and estimates the total [cost](cost) and [time](time) required for the job. 
An [estimate](Estimate) has a unique [id](id). If the [customer](Customer) accepts the [estimate](Estimate), a [job](Job) is created from the estimate. 
A [job](Job) has a unique [number](num) is scheduled for a certain [date](repairDate). 
Information on the [car](Car) is recorded such as the car [license plate number](licnum) (unique), [make](make), [model](model), [year](year), and the customer [name](custName) and [address](custAddress). 
A car may come in for service multiple times (may have multiple jobs). 
A [job](Job) is divided into a list of [repairs](Repair). Each [repair](Repair) has a [number](num), [part cost](partCost) and [description](description). 
A repair may be [done by](WorksOn) one or more mechanics, who can work for different amounts of [time](time). A [mechanic](mechanic) has a unique [name](name) and an [hourly rate](hourlyRate). 
The [labor cost](laborCost) of a mechanic [working on](WorksOn) a repair is calculated using his time and the mechanic hourly rate.','Autoshop',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Estimate| id {PK}; cost; time]
[Job| num {PK}; repairDate]
[Repair| num; partCost; description]
[Mechanic| name {PK}; hourlyRate]
[Car| licnum {PK}; make; model; year; custName; custAddress]
[WorksOn| time; laborCost]
[Mechanic] 1..1 - 0..*[Estimate]
[Estimate] 1..1 - 0..1[Job]
[Estimate] 1..* - 1..1[Car]
[Job] 1..* - 1..1[Car]
[Job] 1..1 - 1..*[Repair]
[Mechanic] 1..1 - 0..*[WorksOn]
[Repair] 1..1 - 1..*[WorksOn]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Autoshop'));

-- 2. Banks question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Draw the ER diagram for a database to store information about all banks with branches. 
Each [bank](Bank) has a unique [federal code](code), [name](name), and [corporate address](address). 
Banks can have numerous [branches](Branch), each with a unique [branch code](specialCode) and an [address](address). 
A [customer](Customer) is identified by [social security number](ssn) and also has a [name](name), [phone number](phone), and [address](address). 
A customer may have multiple [loans](Loan) or [savings accounts](Account) which may be at different branches. 
A customer is not affiliated with a branch directly, only indirectly if they have a [loan](Loan) or [account](Account) at that branch. 
Each [loan](Loan) has a [loan number](number) (unique only for a branch) and a loan [amount](amount). 
Each [savings account](Account) has an [account number](number) (unique only for a branch) and a [balance](balance). 
A loan or account can only belong to a single customer and a single branch.
','Banks',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Bank|code {PK};name;address]
[Branch|code {PK};address]
[Customer|ssn {PK};name;phone;address]
[Loan|number {PPK};amount]
[Account|number {PPK};balance]
[Bank]1..1 - 1..*[Branch]
[Branch]1..1 - 0..*[Account]
[Branch]1..1 - 0..*[Loan]
[Account]0..* - 1..1[Customer]
[Loan]0..* - 1..1[Customer]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Banks'));

-- 3. Claim question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'A [Person](Person) is identified by [social security number](socialsecurity). The person [name](name) and [address](address) must be recorded.
[Cars](Car) are identified by [license plate](licence) and [state](state). For each car, the [model](model), [make](make), and [year](year) is recorded.
A [claim](Claim) has a unique [id](claimid). Also store a [policy number](policynum) and [description](description).
A [car](Car) is owned by a single [person](Person). A person may own multiple cars.
A [claim](Claim) has multiple [line items](LineItem). Each [line item](LineItem) involves a particular person and car involved in the claim. A [l]ine item](LineItem) should store the [date](date) it was created and the [amount](amount) claimed. A line item is identified by its creation date and the claim id it is associated with.
Multiple [payments](Payment) may be made for a claim to the person involved in the claim with values for [amount](amount) and [date](date) of payment.
Draw the ER diagram for this database and convert it a into relational schema. This time create the schema using SQL DDL and make sure to define primary keys and foreign keys.
','Claim',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Person|socialsecurity {PK};name;address]
[Car|licence {PK};state {PK};model;make;year]
[Claim|claimid {PK};policynum;description]
[Lineitem|date {PPK};amount]
[Payment|amount;date {PPK}]
[Person]1..1 - 0..*[Car]
[Person]1..1 - 0..*[Payment]
[Person]1..1 - 0..*[Lineitem]
[Car]1..1 - 0..*[Lineitem]
[Lineitem]0..* - 1..1[Claim]
[Payment]0..* - 1..1[Claim]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Claim'));

-- 4. Congress question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Representatives during the current two year congressional session. 
The database needs to keep track of each U.S. [State](State) [name](name) including [region](Region). 
The [region](Region) has a [name](name) from the domain of {Northeast, Midwest, Southeast, Southwest, and West} and a [description](description) of the region. 
Each [congressperson](Congressperson) in the House is described by [name](name), [district](district) represented, [start date](startdate), and political [party](party). 
Each [state](State) is represented by at least one [congressperson](Congressperson). 
The database keeps track of each [bill](Bill) (proposed law) including bill [name](name), [date](votedate) of vote, [passed or failed](status), and the sponsor [congressperson](Congressperson) of the bill. 
The database keeps track of how each [congressperson](Congressperson) [voted on](VotesOn) each bill [{Yes, No, Abstain, Absent}](vote). State clearly any assumptions.
','Congress',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[State|name {PK}]
[Region|name {PK};description]
[Congressperson|name {PK};district {PK};startdate;party]
[Voteson|vote]
[Bill|name {PK};votedate;status]
[Region]1..1 - 1..*[State]
[State]1..1 - 1..*[Congressperson]
[Congressperson]1..1 - 0..*[Bill]
[Voteson]0..* - 1..1[Bill]
[Congressperson]1..1 - 0..*[Voteson]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Congress'));

-- 5. Drug question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'
The ACME chain of pharmacies agrees to pay you to design and implement a database based on the following information:

[Patients](Patient) are indentified by [SSN](ssn), and their [names](name), [addresses](address), and [ages](age) must be recorded.
[Doctors](Doctor) are identified by [SSN](ssn). For each [doctor](Doctor), the [name](name), [specialty](specialty), and [years of experience](experience) are recorded.
For each [drug](Drug), the trade [name](name) and [formula](formula) must be recorded. The trade name identifies a drug uniquely.
Each [pharmacy](Pharmacy) has a [name](name), [address](address), [phone number](phone), and a unique [id](id).
Every [patient](patient) has only one primary physician. Every [doctor](doctor) has at least one [patient](patient).
Each [pharmacy](pharmacy) [sells](sells) several [drugs](drug) and has a [price](price) for each. A drug could be [sold at](sells) several pharmacies, and the price could vary from one pharmacy to another.
[Doctors](doctor) prescribe [drugs](drug) for patients. A [patient](patient) could obtain drug [prescriptions](prescription) from multiple doctors. Each [prescription](prescription) has a [date](date) and a [quantity](quantity) associated with it. You can assume that, if a doctor prescribes the same drug for the same patient more than once, only the last such prescription needs be stored.
[Supervisors](supervisor) manage each pharmacy. Every [supervisor](supervisor) has a [name](name) and [id](id). A [supervisor](supervisor) manages only one [pharmacy](pharmacy), and each pharmacy always has one supervisor.
','Drug',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Patient|ssn {PK};name;address;age]
[Doctor|ssn {PK};name;specialty;experience]
[Drug|name {PK};formula]
[Pharmacy|id {PK};name;address;phone]
[Sells|price]
[Prescription|date;quantity]
[Supervisor|name;id {PK}]
[Patient]1..* - 1..1[Doctor]
[Doctor]1..1 - 0..*[Prescription]
[Patient]1..1 - 0..*[Prescription]
[Drug]1..1 - 0..*[Prescription]
[Drug]1..1 - 0..*[Sells]
[Pharmacy]1..1 - 1..*[Sells]
[Pharmacy]1..1 - 1..1[Supervisor]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Drug'));

-- 6. Fishstore question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Construct a database design in UML for a fish store where:

A fish store maintains a number of [aquaria (tanks)](tank), each with a [number](number), [name](name), [volume](volume) and [color](color).
Each [tank](tank) contains a number of [fish](fish), each with an [id](id), [name](name), [color](color), and [weight](weight).
Each [fish](fish) is of a particular [species](species), which has a [id](id), [name](name), and [preferred food](preferredFood).
Each individual [fish](fish) has a number of [events](event) in its life, involving a [date](date) and a [note](note) relating to the event.
','Fishstore',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Tank|number {PK};name;volume;color]
[Fish|id {PK};name;color;weight]
[Species|id {PK};name;preferredFood]
[Event|date {PPK};note]
[Tank]1..1 - 0..*[Fish]
[Fish]1..* - 1..1[Species]
[Fish]1..1 - 0..*[Event]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Fishstore'));

-- 7. Football question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'The league will have multiple [teams](team), each with a unique [team name](name). 
For each [game](game) played, there is a [home team](homeTeam), an [away team](awayTeam), [home points](homePoints), [away points](awayPoints), and a [date](gameDate). 
All [teams](team) play multiple home and away games per season. 
The teams all have [players](player) that are identified by [team name](name) and [jersey number](number). Also store a player [name](name). 
The [team name](name) and [number](number) will be unique for each [player](player), while their [name](name) may not be unique. 
Each player ISA [Runningback](runningback) or ISA [Quarterback](quarterback) (Add ISA constraints). 
Each running back has a [type](type) {fullback or halfback}. 
Each quarterback has a [status](status) {starter, backup}. 
[Statistics](QBGameStats) are compiled for each [game](game) for each [player](player). 
The [Runningback statistics]()will include [carries](carries), [yards](yards), and [fumbles](fumbles). 
The [quarterback statistics](QBGameStats) include [passes](passes), [yards](yards), and [interceptions](interceptions). 
In addition, each team is represented by a single [coach](coach). 
A [coach](coach) can coach only one [team](team). Keep track of each coach [name](name) and [salary](salary).
','Football',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Coach| name{PK}; salary]
[Team| name{PK}]
[Player| name; number{PPK}]
[Game| gameDate{PPK}; homePoints; awayPoints]
[Runningback| type]
[Quarterback| status]
[QBGameStats| yards]
[PlaysIn| carries; yards; fumbles]
[Coach]1..1 - 1..1[Team]
[Player]1..* - 1..1[Team]
[Team]1..1 - 0..*[Game]
[Team]1..1 - 0..*[Game]
[Quarterback]1..1 - 0..*[QBGameStats]
[Game]1..1 - 0..*[QBGameStats]
[Game]1..1 - 0..*[PlaysIn]
[RunningBack]1..1 - 0..*[PlaysIn]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Football'));

-- 8. Game question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Design an ER diagram in UML format for a game database given these details:

A [publisher](publisher) is identified by [name](name) and [releases](releases) [games](game). A [game](game) may be released by multiple [publishers](publisher), and each [publisher](publisher) gets credit for a [percent](percent) of the game. (e.g. Publisher A 60%, Publisher B 40%).
A [game](game) is identified by [id](id) and also has a [name](name). 
A [game](game) has one [category](category), and a [category](category) may describe multiple [games](game). A [category](category) is identified by an [id](id) and has a [name](name). A [category](category) may also have multiple [subcategories](category).
A [player](player) is identified by a [userid](userId) and also has a [name](name) and [age](age). A [player](player) may own multiple [games](game), and a [game](game) may be owned by multiple [players](player).
A [session](session) is a particular player playing a game, and the [start time](startTime) is used to identify between sessions of the same game and player combination.
During a [session](session), [stats](stats) are recorded. For a particular [session](session), the [name of the stat](statName) identifies it, and a [value](value) is stored for this statistic.
','Game',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Publisher|name {PK}]
[Releases|percent]
[Game|id {PK};name]
[Category|id {PK};name]
[Player|userId {PK};name;age]
[Session|startTime {PPK}]
[Stats|statName {PPK};value]
[Publisher]1..1 - 0..*[Releases]
[Releases]0..* - 1..1[Game]
[Game]0..* - 1..1[Category]
[Category]1..1 - 0..*[Category]
[Game]1..1 - 0..*[Session]
[Game]0..* - 0..*[Player]
[Session]0..* - 1..1[Player]
[Session]1..1 - 0..*[Stats]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Game'));

-- 9. Hospital question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'The hospital has [departments](department) which have a unique [name](departmentName) and also a [description](description).
The hospital has [doctors](doctor). Each [doctor](doctor) is assigned a unique [id](doctorId) and has a [name](name). 
A [doctor](doctor) may [work in](worksIn) multiple [departments](department). In each [department](department) a doctor [works](worksIn), they are given a [position title](positionTitle).
[Patients](patient) come to the [hospital](hospital) and are assigned a unique [id](patientId).  Also store their [name](name) and [age](age).
A list of [drugs](drug) is maintained. Each [drug](drug) is identified by a [UPC code](upcCode) and has a [name](name).
A [patient](patient) [visits](visit) the [hospital](hospital). Each [visit](visit) is identified by the patient id, doctor id, and the [date](date) together.
At a [visit](visit), zero or more [tests](test) are run. Each [test](test) has a unique [name](testName), and also a [cost](cost) and an [outcome](outcome). A particular [test](test) is run only once per [visit](visit).
A [doctor](doctor) may [prescribe](prescription) a [drug](drug) for a [patient](patient). Each [prescription](prescription) is for a single [patient](patient) by a single [doctor](doctor) for a single [drug](drug) and also contains a [dosage](dosage) and [prescription date](prescriptionDate).
','Hospital',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Department|departmentName {PK};description]
[Doctor|doctorId {PK};name]
[WorksIn|positionTitle]
[Patient|patientId {PK};name;age]
[Drug|upcCode {PK};name]
[Visit|date {PPK}]
[Test|testName {PPK};cost;outcome]
[Prescription|dosage;prescriptionDate]
[Department]1..1 - 0..*[WorksIn]
[Doctor]1..1 - 0..*[WorksIn]
[Doctor]1..1 - 0..*[Prescription]
[Doctor]1..1 - 0..*[Visit]
[Test]0..* - 1..1[Visit]
[Patient]1..1 - 0..*[Visit]
[Patient]1..1 - 0..*[Prescription]
[Drug]1..1 - 0..*[Prescription]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Hospital'));

-- 10. Hotel question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'1.	There are many hotels in the chain. Each [hotel](hotel) has a [name](name), a street address (which is made up of a [street number](streetNumber), [street name](streetName), [city](city), [state](state), and [postal code](postalCode)), a [home page URL](webAddress) (Web address), and a [primary phone number](phoneNumber).
2.	Each [hotel](hotel) consists of a set of [rooms](room) arranged on various [floors](floor). Each [room](room) has an [identifier](roomId) which is unique within that [hotel](hotel). Most of the time, rooms are numbered (e.g. 690), but they may be given a name (e.g. Presidential Suite) instead, so long as the name or number is unique within the hotel. [Floors](floor) are [numbered](floorNum). For simplicity, assume that each [room](room) is on only one [floor](floor).
3.	For each [room](room), it is also necessary to keep track of [how many beds](numBeds) it has, as well as whether [smoking is allowed](smokingRoom) in the room. This information is used to help match guests to rooms with desired characteristics.
4.	When a [guest](guest) plans to stay at a [hotel](hotel), he or she makes a room [reservation](reservation) at the desired [hotel](hotel). Each [reservation](reservation) indicates information about the [guest](guest), the desired [arrival](arrivalDate) and [departure dates](departureDate), as well as preferences that aid in selecting the right kind of room for that guest: whether the room should be [smoking or non-smoking](smokingRoom), the [number of beds](numBeds), and whether the room should be on a [high floor or a low floor](highOrLowFloor). These room preferences are optional, and are not included with every reservation; some guests are willing to take any available room, while some only care about some preferences but not others.
5.	Also required with each [reservation](reservation) is information about a [credit card](creditCard) that is used to secure the reservation; credit cards are indicated by a [credit card number](creditCardNum) (which is a sequence of up to 16 digits) and an [expiration date](creditCardExpiry) (a month and a year, such as "January 2020").
6.	At any given time, a [guest](guest) may have multiple [reservations](reservation). A [reservation](reservation) is for a single [room](room).
7.	For each [guest](guest), the database must store the guest [first](firstName), [middle](middleName), and [last names](lastName), [street address](streetAddress), [email address](email), and three phone numbers ([home](homePhone), [work](workPhone), [cell](cellPhone)). Email addresses and the phone numbers are optional, while the other information is required. Note that if multiple [people](guest) stay in a [room](room), we are only storing information about the one [person](guest) who reserved the [room](room).
8.	A single [invoice](invoice) is [generated](openDate) for a [reservation](reservation) at the [hotel](hotel), detailing the individual [charges](invoiceCharge) accrued by the [guest](guest). These [charges](invoiceCharge) include not only the regular room rate, but also applicable taxes, as well as charges at the hotel restaurants, bars, spas, shops, and so on. An [invoice](invoice) is displayed either in printed or Web-based form as a sequence of line items, with each line item consisting of a [description](description) and an [amount](amount), such as "Hotel Cafe $29.75". Note that the database does not keep track of, say, the costs of items on the restaurant menu or the cost of renting each room at various times throughout the year; it is assumed that another software system provides this information to our database, since our system only handles reservations and billing.
9.	When a [guest](guest) [pays](transactionId) his or her bill or a portion of his or her bill a line item is added to the invoice that indicates [how much was paid](amount), and in what [form](chargeType) the payment was made (e.g. "Visa $-500.00", in the case of a $500 payment made using a Visa credit card).
10.	At the bottom of each invoice is a [total balance](totalBalance), which is the sum of the amounts in each of the line items, including both [charges and payments](invoiceCharge). An invoice is considered [paid](closeDate) if the amount is $0.00.
','Hotel',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Hotel| name{PK}; streetNumber; streetName; city; state; postalCode; webAddress; phoneNumber]
[Floor| number{PPK}]
[Room| identifier{PPK}; numbed; isSmokingRoom]
[Reservation| arrivalDate{PPK}; departDate; smokingRoom; numBeds; highOrLowFloor; creditCardType; creditCardNum; creditCardExpiry]
[Customer| id{PK}; firstName; middleName; lastName; address; city; state; country; postalCode; homePhoneNumber; workPhoneNumber; cellPhoneNumber; emailAddress]
[Invoice| id{PK}; openDate; closeDate; totalBalance]
[InvoiceCharge| transactionId{PPK, auto}; chargeType; description; amount]
[Hotel]1..1 - 1..*[Floor]
[Hotel]1..1 - 1..*[Room]
[Hotel]1..1 - 0..*[Reservation]
[Floor]1..1 - 0..*[Room]
[Reservation]0..* - 1..1[Room]
[Reservation]1..1 - 1..1[Invoice]
[Reservation]0..* - 1..1[Customer]
[InvoiceCharge]0..* - 1..1[Invoice]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Hotel'));

-- 11. Inventory question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'The logistics manager at your company wants to design a database to store the following information about warehouses.
Each [warehouse](warehouse) has a unique [warehouse name](warehouseName). Also, store the [city](city) and [state](state) of the warehouse. 
[Products](product) have a unique [product id](productId), [name](name), and [price](price). 
Store the [volume](inventory)(inventory) of each [product](product) [at each](stores) [warehouse](warehouse). 
Not all [products](product) are [stored at](stores) each [warehouse](warehouse) and a [warehouse](warehouse) may not [store](stores) all [products](product).
A [shipment](shipment) identified by a unique [shipment number](shipmentNumber) has a [shipper name](shipperName) and [contact](contact). A [shipment](shipment) is filled from only one [warehouse](warehouse). 
Each [shipment](shipment) [contains](contains) at least one [product](product). Each [product](product) [shipped](contains) has a [quantity](quantity).
A [shipment](shipment) goes to a single [customer](customer) where each [customer](customer) is identified by a [customer number](customerNum), [name](name), and [address](address).
','Inventory',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Warehouse|warehouseName {PK};city;state]
[Product|productId {PK};name;price]
[Stores|inventory]
[Shipment|shipmentNumber {PK};shipperName;contact]
[Contains|quantity]
[Customer|customerNum {PK};name;address]
[Shipment]0..* - 1..1[Warehouse]
[Shipment]1..1 - 1..*[Contains]
[Shipment]0..* - 1..1[Customer]
[Contains]0..* - 1..1[Product]
[Warehouse]1..1 - 0..*[Stores]
[Stores]0..* - 1..1[Product]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Inventory'));
    
-- 12. MedicalSystem question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'There are multiple [hospitals](hospital) in the medical system. A [hospital](hospital) is identified by its [name](hospitalName) and has a [location](location).
A [doctor](doctor) is identified by their [medical number](medicalNum) and has a [name](name). Each [hospital](hospital) has a single [doctor](doctor) as a manager, and a [doctor](doctor) may manage only one [hospital](hospital).
[Doctors](doctor) are [located in](locatedIn) [hospitals](hospital). A doctor may be [located in](locatedIn) more than one [hospital](hospital). A doctor located at a hospital has an [office number](officeNum) and a [salary](salary) paid by that [hospital](hospital).
A [patient](patient) is identified by their [health id](healthId) and also has a [name](name) and [gender](gender).
A [patient](patient) [visits](visit) a [doctor](doctor) at a particular [hospital](hospital). Each [visit](visit) is identifed by its own [id](visitId) and also has a [visit date](date).
At a [visit](visit) zero or more [tests](test) are run each with a [cost](cost) and an [outcome](outcome). Each [test](test) is identified for a particular [visit](visit) by [name](testName).','MedicalSystem',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Hospital|hospitalName {PK};location]
[Doctor|medicalNum {PK};name]
[LocatedIn|officeNum;salary]
[Patient|healthId {PK};name;gender]
[Visit|visitId {PK};date]
[Test|testName {PPK};cost;outcome]
[Hospital]1..1 - 1..1[Doctor]
[Hospital]1..1 - 0..*[LocatedIn]
[Doctor]1..1 - 0..*[LocatedIn]
[Hospital]1..1 - 0..*[Visit]
[Doctor]1..1 - 0..*[Visit]
[Patient]1..1 - 0..*[Visit]
[Test]0..* - 1..1[Visit]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'MedicalSystem'));

-- 13. MusicDB question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'An [artist](artist) is a musician who records [songs](song). 
An [artist](artist) has a [record label](label). An [artist](artist) is identified by an [id](artistId) that is specific to their [record label](label). That is, each [record label](label) assigns its own [ids](artistId). Also, record an [artist’s](artist) [name](name) and [age](age).
A [record label](label) has a unique [name](labelName) and an [address](address).
A [song](song) is recorded by one or more [artists](artist) and is uniquely identified by an [id](songId) field and has a [title](title).
A [song](song) [is on](isOn) one or more [albums](album) with a [track number](trackNum) and [duration](duration).  (Note: Assume an artist can put the same song on multiple albums, but any song change is given a new id.)
An [album](album) is a collection of [songs](song) with a [name](albumName). Track the number of [sales](sales) of an [album](album). An [album](album) may be [associated with](releases) multiple [artists](artist) and is identified by an [UPC code](upcCode). An [artist](artist) [on an](releases) [album](album) is given a [number](artistNum) (first artist, second artist, etc.).
An [album](album) is classified in a single [genre](genre) (rap, classical, etc.). A [genre](genre) is identified by [name](genreName) and also has a [description](description).
','MusicDB',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Artist|artistId {PPK};name;age]
[Song|songId {PK};title]
[Label|labelName {PK};address]
[IsOn|trackNum;duration]
[Album|upcCode {PK};albumName;sales]
[Releases|artistNum]
[Genre|genreName {PK};description]
[Label]1..1 - 0..*[Artist]
[Artist]1..* - 0..*[Song]
[Artist]1..1 - 0..*[Releases]
[Releases]1..* - 1..1[Album]
[Song]1..1 - 1..*[IsOn]
[IsOn]1..* - 1..1[Album]
[Album]0..* - 1..1[Genre]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'MusicDB'));

-- 14. Project question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'A [Customer](customer) is identified by an auto-increment [id](customerId). Other attributes include [first name](firstName), [last name](lastName), [email](email), [phone number](phone), [street address](streetAddress), [city](city), [province](province), (postal code)(postCode), and [country](country). A [Customer](customer) also has a [user id](userId) (unique) and [password](password).
A [customer](customer) may have one or more [payment methods](paymentMethod). A [Payment Method](paymentMethod) has an auto-increment [id](paymentMethodId) for a key, a [payment method type](type) (PayPal, Visa, etc.), [payment number](number), and [payment expiry date](expiryDate).
An [Order](orderSummary) is placed by one [customer](customer). A [customer](customer) may have multiple [orders](orders). An [Order](orderSummary) has an auto-increment [id](orderId), order [date](date), and [total order amount](totalAmount) (e.g. $55.75). Also store the [shipment address](shipToAddress), [city](shipToCity), [state](shipToState), [country](shipToCountry), and [postal code](shipToPostcode). Use [OrderSummary](orderSummary) as entity/table name as order is a keyword in SQL.
The store sells [products](product). A [Product] has an auto-increment [id](productId), [name](name), [price](price), [image URL](imageURL) (string), [image](image) (BLOB), and [description](description).
A [product](product) has a [category](category). A [category](category) has one or more [products](product). A [Category](category) has an auto-increment [id](categoryId) and [name](name).
[Products](product) are [part of](orderProduct) an [order](orderSummary). An [order](orderSummary) may have one or more [products](product). For each [product](product) [in an](orderProduct) [order](orderSummary) track the [quantity](quantity) and [price](price).
An [order](orderSummary) is shipped with a [shipment](shipment). A [Shipment](shipment) has an auto-increment [id](shipmentId), a [shipment date](date), and a [description](description). A [shipment](shipment) contains only one [order](order).
A [Warehouse](warehouse) contains [products](product). A [product](product) may be [stored at](productInventory) multiple [warehouses](warehouse)  with different [inventory values](quantity). A [shipment](shipment) will be sent from only one [warehouse](warehouse). A [Warehouse](warehouse) has an auto-increment [id](warehouseId) and a [name](name).
For each [customer](customer), track their [shopping cart](inCart) which will contain one or more [products](product)  each with a [quantity](quantity) and [price](price).
A [product](product) may have [reviews](review) by [customers](customer). A [Review](review) by a [customer](customer) on a [product](product) has an auto-increment [id](reviewId), [rating](rating) (1 to 5), [comment](comment), and review [date](date). A [customer](customer) does not have to buy a [product](product) in order to provide a [review](review). A [customer](customer) may [review](review) a [product](product) more than once.
','Project',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[PaymentMethod| paymentMethodId{PK}; type; number; expiryDate]
[Customer| customerId{PK}; firstName; lastName; email; phone; address; city; state; postCode; country; userId; password]
[OrderSummary| orderId{PK}; date; totalAmount; shiptoAddress; shiptoCity; shiptoState; shiptoPostcode; shiptoCountry]
[Review| reviewId{PK}; rating; comment; date]
[InCart| quantity; price]
[OrderProduct| quantity; price]
[Category| categoryId{PK}; name]
[Product| productId{PK}; name; price; imageURL; image; description]
[Shipment| shipmentId{PK}; date; description]
[ProductInventory| quantity]
[Warehouse| warehouseId{PK}; name]
[Customer]1..1 - 0..*[PaymentMethod]
[Customer]1..1 - 0..*[OrderSummary]
[Customer]1..1 - 0..*[InCart]
[Customer]1..1 - 0..*[Review]
[OrderSummary]1..1 - 0..*[OrderProduct]
[OrderSummary]1..1 - 1..1[Shipment]
[Review]0..* - 1..1[Product]
[InCart]0..* - 1..1[Product]
[OrderProduct]0..* - 1..1[Product]
[Category]1..1 - 1..*[Product]
[ProductInventory]0..* - 1..1[Product]
[ProductInventory]0..* - 1..1[Warehouse]
[Shipment]0..* - 1..1[Warehouse]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Project'));

-- 15. Publisher question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Construct a database design in UML for an app store described below.

A [Publisher](publisher) where each [publisher](publisher) is identified by an [id](id) and has a [name](name).
A [Category](category) where each [category](category) has an [id](id), a [name](name), and may have a parent [category](category).
An [App](app) storing each [app](app) that is identified by a field called [id](id) and other attributes include [name](name) and [description](description). An [App](app) is created by one [Publisher](publisher). A [Publisher](publisher) may publish multiple [Apps](app). An [App](app) has a [Category](category).
A [AppVersion](appVersion) stores each version of the app. An [AppVersion](appVersion) is associated with exactly one [App](app). Use a [version](version) field to identify between [versions](appVersion) of the same [App](app). Each [AppVersion](appVersion) has a [release date](releaseDate), a [rating](rating), a [price](price), and a [description](description).
A [AppVersionReview](appVersionReview) stores [ratings](rating) for each application version. Each [instance](appVersionReview) applies to a single [AppVersion](appVersion), and different [reviews](appVersionReview) are identified by [reviewer](reviewer) attribute (which is name of reviewer). There is also a [reviewDate](reviewDate), [rating](rating), and [review](review).','Publisher',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Publisher|id {PK};name]
[Category|id {PK};name]
[App|id {PK};name;description]
[AppVersion|version {PPK};releaseDate;rating;price;description]
[AppVersionReview|rating;reviewer {PPK};reviewDate;review]
[Publisher]1..1 - 0..*[App]
[App]1..1 - 0..*[AppVersion]
[App]0..* - 1..1[Category]
[AppVersion]1..1 - 0..*[AppVersionReview]
[Category]0..* - 1..1[Category]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Publisher'));
-- 16. Student question
INSERT INTO "questions_question" ("created","question","title","maximum_grade","other_marking_criteria","custom_css","created_by_id","question_template_id")
VALUES (NOW(),'Design an ER diagram for a university:
The database needs to keep track of each [Instructor](instructor) with [id](id), [name](name), and [address](address). Each [instructor](instructor) works for one [department](department) and each [department](department) has at least one [instructor](instructor).
The [departments](department) have a unique [id](id) and a [name](name). 
[Courses](course) are offered by a single [department](department) and have a [number](courseNum) unique to each [department](department). Store the [course name](courseName), [credits](credits), and [description](description).
Each [course](course) has at least one [section](section). A [section](section) is identified using its associated [course number](courseNum), [section number](sectionNum), [year](year), and [semester](semester). Also store the [size](size) of the [section](section). 
[Students](student) have [student ids](studentId) and [names](name). Each [student](student) has a single [instructor](instructor) as an advisor. 
[Students](student) enroll in one or more [sections](section). A [section](section) must have five [students](student) or it is cancelled. A [section](section) is taught by at least one [instructor](instructor).
','Student',10,'','',1,1);


INSERT INTO "questions_potentialanswer" ("answer","is_correct","question_id")
VALUES ('[Instructor|id {PK};name;address]
[Department|id {PK};name]
[Course|courseNum {PPK};courseName;credits;description]
[Section|sectionNum {PPK};year {PPK};semester {PPK};size]
[Student|studentId {PK};name]
[Instructor]1..* - 1..1[Department]
[Instructor]1..1 - 0..*[Student]
[Student]1..* - 1..*[Section]
[Instructor]1..* - 0..*[Section]
[Department]1..1 - 1..*[Course]
[Course]1..1 - 1..*[Section]',TRUE,
    (SELECT q.id FROM questions_question as q
    WHERE q.title = 'Student'));