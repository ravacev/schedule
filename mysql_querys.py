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
    DownUsers AS 'Afectacion'
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
    status.StatusDesc = 'PENDIENTE'
'''