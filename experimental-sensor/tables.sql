CREATE TABLE experimental(
    temperature float,
    EventProcessedUtcTime datetime,
    EventEnqueuedUtcTime datetime
)

select *
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='experimental';


CREATE TABLE telemetry (
    id INT PRIMARY KEY IDENTITY (1, 1),
    temperature int NOT NULL,
    humidity int NOT NULL,
    timestamp DATETIME
);

CREATE TABLE [dbo].[vmperf](

	[eventTime] [datetime] NOT NULL,

	[vmname] [nvarchar](max) NOT NULL,

	[location_continent] [nvarchar](50) NULL,

	[location_country] [nvarchar](50) NULL,

	[location_province] [nvarchar](50) NULL,

	[location_city] [nvarchar](50) NULL,

	[CounterName] [nvarchar](max) NULL,

	[CounterValue] [float] NULL

);
