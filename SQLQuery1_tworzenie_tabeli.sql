
-- model do django z istniejacej databazy robi sie tak: --
-- python manage.py inspectdb > models.py

-- a nastepnie:
-- python run manage.py migrate

-- ***************************************************************** --

CREATE TABLE dbo.Driver
(
	ID int IDENTITY(1,1) PRIMARY KEY	-- primary key zapewni ze id bedzie unikalne (nie moze byc drugie takie same)
)
GO

ALTER TABLE dbo.Driver  
   ADD first_name			 nvarchar(50)   NULL,
       surname				 nvarchar(50)   NULL,
	   driver_id			 int			NULL,
	   offense_cnt			 int			DEFAULT(0),
	   total_driving_time	 time			DEFAULT('00:00:00')
GO	

ALTER TABLE dbo.Driver   
   ADD driving_rating float DEFAULT 10.0   
   CONSTRAINT CHK_driving_rating   
   CHECK (driving_rating >= 0.0 AND driving_rating <= 10.0);  
GO		

-- ***************************************************************** --

CREATE TABLE dbo.Cars
(
	ID int IDENTITY(1,1) PRIMARY KEY	
)
GO

ALTER TABLE dbo.Cars
	ADD  car_brand				 nvarchar(50)	NULL,
		 plate_number			 nvarchar(10)	NULL,
		 car_VIN				 nvarchar(17)	NULL,
		 vehicle_year			 int			NULL,
		 total_driving_time		 time			DEFAULT('00:00:00'),
		 car_mileage			 decimal(8,1)	DEFAULT(0.0)

GO

-- ***************************************************************** --

CREATE TABLE dbo.Trips
(
	ID			INT IDENTITY(1,1)	PRIMARY KEY,
)
GO

ALTER TABLE dbo.Trips
ADD 
	driver_id   INT					NOT NULL,
	car_id	    INT         		NOT NULL,	    
	gpx_files   nvarchar(50)		NOT NULL

GO

 -- DROP TABLE dbo.Trips

-- ***************************************************************** --

CREATE TABLE dbo.Trips (
    TrasaID INT IDENTITY(1,1) PRIMARY KEY,
    PunktID INT,
    WspolrzednaX DECIMAL(9,6),
    WspolrzednaY DECIMAL(9,6),
    Czas DATETIME
)
GO

