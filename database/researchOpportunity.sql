CREATE DATABASE IF NOT EXISTS ResearchOpportunity;
USE ResearchOpportunity;

CREATE TABLE Opportunities(
	ID INT PRIMARY KEY AUTO_INCREMENT,
    ResearchTitle VARCHAR(255) NOT NULL,
    ResearchDescription VARCHAR(255) NOT NULL,
    ResearchArea VARCHAR(255) NOT NULL,
    FacultyMemberName VARCHAR(255) NOT NULL,
    Department VARCHAR(255) NOT NULL,
    RequiredSkills TEXT NOT NULL,
    NumberOfAvailablePosition INT NOT NULL,
    ApplicationDeadline TIMESTAMP NOT NULL,
    Status ENUM('Open','Closed') NOT NULL DEFAULT 'Open'
);
