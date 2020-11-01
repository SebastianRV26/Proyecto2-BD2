select * from 
information_schema.table_privileges;

select * from 
information_schema.column_privileges
where table_schema='optimizacion' and table_name='rios'
order by column_name, privilege_type;

--Postgres: listado de índices
select * from pg_indexes where tablename='patentes';

--SQLserver: listado de índices
select s.name, t.name, i.name, c.name from sys.tables t
inner join sys.schemas s on t.schema_id = s.schema_id
inner join sys.indexes i on i.object_id = t.object_id
inner join sys.index_columns ic on ic.object_id = t.object_id
inner join sys.columns c on c.object_id = t.object_id and
        ic.column_id = c.column_id