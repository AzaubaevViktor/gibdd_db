from ora_adapter import Oracle
Oracle.execute("""
CREATE OR REPLACE FUNCTION NUM_TO_REG(NUM IN NUMBER) RETURN VARCHAR2
  IS
  REG VARCHAR(6);
  X NUMBER;
  BEGIN
    X := NUM;
    REG := CHR(MOD(X, 25) + 97);
    X := X / 25;
    REG := REG || CHR(MOD(X, 9) + 48);
    X := X / 9;
    REG := REG || CHR(MOD(X, 9) + 48);
    X := X / 9;
    REG := REG || CHR(MOD(X, 9) + 48);
    X := X / 9;
    REG := REG || CHR(MOD(X, 25) + 97);
    X := X / 25;
    REG := REG || CHR(MOD(X, 25) + 97);
    RETURN (REG);
  END NUM_TO_REG;
""").close()

Oracle.execute("""
CREATE OR REPLACE FUNCTION GET_REG_NUM(VT_id IN INTEGER) RETURN VARCHAR2
  IS
  reg_val NUMBER;
  CURSOR interval IS
    SELECT * FROM FreeRegNum WHERE vehicle_type_id=VT_id;
  row_gt FreeRegNum%ROWTYPE;
  BEGIN
    OPEN interval;
    FETCH interval INTO row_gt;
    CLOSE interval;
    reg_val := row_gt.sta;
    UPDATE FreeRegNum
      SET sta = reg_val + 1
        WHERE id=row_gt.id;
    RETURN NUM_TO_REG(reg_val);
  END GET_REG_NUM;
""").close()