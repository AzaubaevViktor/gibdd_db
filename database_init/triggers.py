from ora_adapter import Oracle

Oracle.execute("""
CREATE OR REPLACE TRIGGER VEHICLE_REG_BEFORE
  BEFORE INSERT OR UPDATE ON Vehicle
  FOR EACH ROW
  DECLARE
  reg_number Vehicle.reg_number%type;
  BEGIN
    IF :new.reg_number is NULL THEN
      SELECT GET_REG_NUM() INTO :new.reg_number FROM Dual;
    ELSE
      CHECK_REG_NUM(:new.reg_number);
    END IF;
  END;
""")
