sumAintechView = '''
    SELECT DISTINCT 
	count(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND
    Crew = 'Aintech'
'''
    
sumModifyView = '''
    SELECT DISTINCT 
	COUNT(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND 
    Crew <> 'Aintech'
UNION ALL
	SELECT DISTINCT 
	COUNT(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'SOLUCIONADO'
    AND 
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateDone, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
'''

sumReportStatus = '''
    SELECT DISTINCT 
	COUNT(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
UNION ALL
	SELECT DISTINCT 
	COUNT(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'SOLUCIONADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateDone, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
'''

getReportSem = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
	AND
    status.StatusDesc = 'SOLUCIONADO'
    AND
    DateDone between DATE_ADD(curdate(), INTERVAL - 7 DAY) and DATE_ADD(curdate(), INTERVAL - 1 DAY);
    '''

getSelectN1 = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'POSTERGADO'
	AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(DATE_ADD(CURDATE(), INTERVAL 1 DAY), '%d-%m-%Y');
'''

getSelectN = '''
    SELECT DISTINCT 
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente',  
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y, %k:%ihs') AS 'Ingreso', 
	Priority AS 'Prioridad', 
    AffectClients AS 'Clientes Afectados',  
    datediff(now(), DateDemand) AS 'Demora',
	Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    Town AS 'Ciudad', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y, %k:%ihs') AS 'Resolucion', 
    StatusReason AS 'Motivo'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'POSTERGADO'
	AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(CURDATE(), '%d-%m-%Y')
    ORDER BY
    Team, Ciudad, Demora, Prioridad;
'''

getSumN = '''
    SELECT DISTINCT 
	count(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'POSTERGADO'
	AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(CURDATE(), '%d-%m-%Y');
    '''

getReportGen = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode'''

getSelectSchedule = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    DateDemand BETWEEN '2023-01-01 00:00:00' AND curdate()
    ORDER BY
    status.StatusDesc
'''

getModifyView = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario',
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') AS 'Agendamiento'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND 
    Crew <> 'Aintech'
UNION
	SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario',
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') AS 'Agendamiento'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'SOLUCIONADO'
    AND 
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateDone, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
    ORDER BY Team, Ciudad, Prioridad
    '''
    
getAintechView = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario',
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') AS 'Agendamiento'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND
    Crew = 'Aintech'
    ORDER BY Team, Ciudad, Prioridad
    '''
    
getReportStatus = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'SOLUCIONADO'
    AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    status.StatusDesc <> 'POSTERGADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
UNION
	SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'SOLUCIONADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateDone, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
    ORDER BY Team, Ciudad, Prioridad
    '''
    
getPostergadoView = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    TicketComment AS 'Comentario',
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') AS 'Agendamiento'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'POSTERGADO'
'''

sumPostergadoView = '''
    SELECT DISTINCT 
    count(*)
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc = 'POSTERGADO'
'''

PutUpdateSchedule = '''
UPDATE 
    work, status, napDesc, descZone, crew
SET 
    work.JobID = %s,
    work.TicketID = %s,
    napDesc.Name = %s,
    napDesc.Issue = %s,
    napDesc.Phase = %s,
    napDesc.Coord = %s,
    work.AffectClients = %s,
    status.Priority = %s,
    crew.Crew = %s,
    crew.Partner = %s,
    descZone.City = %s,
    descZone.Town = %s,
    descZone.District = %s,
    status.StatusDesc = %s,
    work.DateDone = %s,
    work.DateSchedule = %s,
    status.StatusReason = %s,
    status.DownUsers = %s,
    status.TicketComment = %s,
    work.UsersID = %s
WHERE
    work.StatusCode = status.StatusCode
    AND
    work.NapCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.workID = %s;
'''

InsertStatus = '''
INSERT INTO `status`
(
`StatusDesc`,
`StatusReason`,
`Priority`,
`DownUsers`,
`TicketComment`
)
VALUES
(
%s,
%s,
%s,
%s,
%s);
'''

InsertCrew = '''
INSERT INTO `crew`
(
`Crew`,
`Partner`,
`Active`)
VALUES
(
%s,
%s,
True);
'''

InsertZone = '''
INSERT INTO `descZone`
(
`City`,
`Town`,
`District`)
VALUES
(
%s,
%s,
%s);
'''

InsertNap = '''
INSERT INTO `napDesc`
(
`Name`,
`Detail`,
`Phase`,
`Issue`,
`Coord`)
VALUES
(
%s,
%s,
%s,
%s,
%s);
'''

InsertWork = '''
INSERT INTO `work`
(`TicketID`,
`JobID`,
`AffectClients`,
`DateDemand`,
`DateDone`,
`DateSchedule`,
`NapCode`,
`UsersID`,
`CrewCode`,
`ZoneCode`,
`StatusCode`)
VALUES
(%s,
%s,
%s,
%s,
%s,
%s,
(SELECT COUNT(*) FROM napDesc),
%s,
(SELECT COUNT(*) FROM crew),
(SELECT COUNT(*) FROM descZone),
(SELECT COUNT(*) FROM status)
);
'''

searchAll = '''
	SELECT DISTINCT JobID AS 'OT', 
	TicketID AS 'Ticket', 
	Name 'NAP', 
	Issue AS 'Inconveniente', 
	Phase AS 'Fase', 
	Coord AS 'Coordenadas', 
	DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
	AffectClients AS 'Clientes Afectados', 
	datediff(now(), DateDemand) AS 'Demora',
	Priority AS 'Prioridad', 
	Crew AS 'Team', 
	Partner AS 'Cuadrilla',
	City AS 'Departamento', 
	Town AS 'Ciudad', 
	District AS 'Barrio', 
	StatusDesc AS 'Estado', 
	DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
	StatusReason AS 'Motivo',
	DownUsers AS 'Afectacion',
    Username AS 'Usuario' FROM work 
	JOIN napDesc, status, crew, descZone, users
	WHERE 
	work.napCode = napDesc.NapCode
	AND
	work.CrewCode = crew.CrewCode
	AND
	work.ZoneCode = descZone.ZoneCode
	AND
	work.StatusCode = status.StatusCode
    AND
    work.UsersID = users.UsersID;
'''

searchTK = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    Username AS 'Usuario'
    FROM work 
    JOIN napDesc, status, crew, descZone, users
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    work.UsersID = users.UsersID
    AND
    TicketID LIKE %s"%"
    '''
    
searchNAP = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    Username AS 'Usuario'
    FROM work 
    JOIN napDesc, status, crew, descZone, users
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    work.UsersID = users.UsersID
    AND
    napDesc.Name LIKE %s"%"
    ORDER BY
    TicketID DESC
    '''
    
searchOT = '''
    SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    Username AS 'Usuario'
    FROM work 
    JOIN napDesc, status, crew, descZone, users
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    work.UsersID = users.UsersID
    AND
    JobID LIKE %s"%"
    '''
    
searchDT = '''SELECT DISTINCT 
    workID,
    JobID AS 'OT', 
    TicketID AS 'Ticket', 
    Name 'NAP', 
    Issue AS 'Inconveniente', 
    Phase AS 'Fase', 
    Coord AS 'Coordenadas', 
    DATE_FORMAT(DateDemand, '%d-%m-%Y') AS 'Ingreso', 
    AffectClients AS 'Clientes Afectados', 
    datediff(now(), DateDemand) AS 'Demora',
    Priority AS 'Prioridad', 
    Crew AS 'Team', 
    Partner AS 'Cuadrilla',
    City AS 'Departamento', 
    Town AS 'Ciudad', 
    District AS 'Barrio', 
    StatusDesc AS 'Estado', 
    DATE_FORMAT(DateDone, '%d-%m-%Y') AS 'Resolucion', 
    StatusReason AS 'Motivo',
    DownUsers AS 'Afectacion',
    Username AS 'Usuario'
    FROM work 
    JOIN napDesc, status, crew, descZone, users
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    work.UsersID = users.UsersID
    AND
    DATE_FORMAT(DateDone, '%d-%m-%Y') LIKE %s"%"
    '''

getResumeSelect = '''
    SELECT DISTINCT 
	statusDesc AS 'Estado',
    count(*) AS 'Cuenta'
    FROM work 
    JOIN napDesc, status, crew, descZone
    WHERE 
    work.napCode = napDesc.NapCode
    AND
    work.CrewCode = crew.CrewCode
    AND
    work.ZoneCode = descZone.ZoneCode
    AND
    work.StatusCode = status.StatusCode
    AND
    status.StatusDesc <> 'POSTERGADO'
	AND
    status.StatusDesc <> 'CANCELADO'
    AND
    status.StatusDesc <> 'ELIMINADO'
    AND
    Crew <> 'Aintech'
    AND
    DATE_FORMAT(DateSchedule, '%d-%m-%Y') = DATE_FORMAT(curdate(), '%d-%m-%Y')
    GROUP BY statusDesc
'''