use timekeeping;
CREATE TABLE `Employee`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `fullname` VARCHAR(255) NOT NULL,
    `phonenumber` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `dataset` VARCHAR(255) NOT NULL,
    `department_id` INT UNSIGNED NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `Timekeeping`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `date` DATE NOT NULL,
    `time_in` DATETIME NOT NULL,
    `time_out` DATETIME NOT NULL,
    `employee_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `Department`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `department_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `timekeeping`.`admin` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `pwd` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`ID`));


ALTER TABLE
    `Timekeeping` ADD CONSTRAINT `timekeeping_employee_id_foreign` FOREIGN KEY(`employee_id`) REFERENCES `Employee`(`id`);
ALTER TABLE
    `Employee` ADD CONSTRAINT `employee_department_id_foreign` FOREIGN KEY(`department_id`) REFERENCES `Department`(`id`);