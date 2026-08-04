-- Function: fires on DDL changes and sends a Postgres NOTIFY
CREATE OR REPLACE FUNCTION notify_schema_change()
RETURNS event_trigger AS $$
BEGIN
  PERFORM pg_notify('schema_changes', json_build_object(
    'event', tg_tag,
    'time', now()
  )::text);
END;
$$ LANGUAGE plpgsql;

-- Event trigger: watches for table-level DDL and calls the function above
CREATE EVENT TRIGGER on_ddl_change
ON ddl_command_end
WHEN TAG IN ('CREATE TABLE', 'DROP TABLE', 'ALTER TABLE')
EXECUTE FUNCTION notify_schema_change();
