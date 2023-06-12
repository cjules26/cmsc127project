-- Drop the database if it exists
DROP DATABASE IF EXISTS `app`;

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `app`;

-- Use the `app` database
USE `app`;

-- Create the PERSON table
CREATE TABLE IF NOT EXISTS `PERSON` (
    `userID` VARCHAR(4) NOT NULL,
    `fName` VARCHAR(30),
    `lName` VARCHAR(30),
    `moneyOwed` DECIMAL(8, 2),
    `moneyLent` DECIMAL(8, 2),
    `borrowerId_fk` VARCHAR(4),
    PRIMARY KEY (`userID`),
    CONSTRAINT `borrower_user`
        FOREIGN KEY (`borrowerId_fk`)
        REFERENCES `PERSON`(`userID`)
);

-- Create the GROUPING table
CREATE TABLE IF NOT EXISTS `GROUPING` (
    `groupID` VARCHAR(4) NOT NULL,
    `groupName` VARCHAR(30),
    `moneyOwed` DECIMAL(8, 2),
    `moneyLent` DECIMAL(8, 2),
    PRIMARY KEY (`groupID`)
);

-- Create the GROUP_MEMBER table
CREATE TABLE IF NOT EXISTS `GROUP_MEMBER` (
    `groupID` VARCHAR(4) NOT NULL,
    `memberID` VARCHAR(4) NOT NULL,
    PRIMARY KEY (`groupID`, `memberID`)
);

-- Create the EXPENSE table
CREATE TABLE IF NOT EXISTS `EXPENSE` (
    `expenseID` VARCHAR(6) NOT NULL,
    `amount` DECIMAL(8, 2),
    `sender` VARCHAR(4),
    `recipient` VARCHAR(4),
    `dateOwed` DATE,
    `datePaid` DATE,
    `userID` VARCHAR(4),
    `groupID` VARCHAR(4),
    PRIMARY KEY (`expenseID`),
    CONSTRAINT `deptfk`
        FOREIGN KEY (`userID`)
        REFERENCES `PERSON`(`userID`),
    CONSTRAINT `groupfk`
        FOREIGN KEY (`groupID`)
        REFERENCES `GROUPING`(`groupID`)
);

-- Insert statements
INSERT INTO `PERSON` VALUES ("U1", "Mario", "Beatles", 700, 0, NULL);
INSERT INTO `PERSON` VALUES ("U2", "Lea", "Smith", 0, 100, "U1");
INSERT INTO `PERSON` VALUES ("U3", "Sophia", "Brown", 0, 100, "U1");
INSERT INTO `PERSON` VALUES ("U4", "Daniel", "Taft", 0, 100, "U1");
INSERT INTO `PERSON` VALUES ("U5", "Olivia", "Davis", 0, 100, "U1");

INSERT INTO `GROUPING` VALUES ("G1", "AAA", 0, 100);
INSERT INTO `GROUPING` VALUES ("G2", "BBB", 0, 100);
INSERT INTO `GROUPING` VALUES ("G3", "CCC", 0, 100);

INSERT INTO `EXPENSE` VALUES ("E1", 100, "U2", "U1", "2021-07-12", NULL, "U2", NULL);
INSERT INTO `EXPENSE` VALUES ("E2", 100, "U3", "U1", "2022-01-12", NULL, "U3", NULL);
INSERT INTO `EXPENSE` VALUES ("E3", 100, "U4", "U1", "2010-01-02", NULL, "U4", NULL);
INSERT INTO `EXPENSE` VALUES ("E4", 100, "U5", "U1", "2021-07-20", NULL, "U5", NULL);
INSERT INTO `EXPENSE` VALUES ("E5", 100, "G1", "U1", "2019-07-12", NULL, "U1", "G1");
INSERT INTO `EXPENSE` VALUES ("E6", 100, "G2", "U1", "2019-07-12", NULL, "U1", "G2");
INSERT INTO `EXPENSE` VALUES ("E7", 100, "U2", "U1", "2021-07-12", "2022-07-20", "U2", NULL);
INSERT INTO `EXPENSE` VALUES ("E8", 100, "U3", "U1", "2021-01-12", "2022-09-26", "U3", NULL);
INSERT INTO `EXPENSE` VALUES ("E9", 100, "U4", "U1", "2021-01-02", "2022-11-19", "U4", NULL);
INSERT INTO `EXPENSE` VALUES ("E10", 100, "G1", "U1", "2021-07-12", "2022-07-20", "U1", "G1");
INSERT INTO `EXPENSE` VALUES ("E11", 100, "G2", "U1", "2021-01-12", "2022-09-26", "U1", "G2");

INSERT INTO `GROUP_MEMBER` VALUES ("G1", "U1");
INSERT INTO `GROUP_MEMBER` VALUES ("G1", "U2");
INSERT INTO `GROUP_MEMBER` VALUES ("G1", "U3");
INSERT INTO `GROUP_MEMBER` VALUES ("G2", "U4");
INSERT INTO `GROUP_MEMBER` VALUES ("G2", "U5");