from ora_adapter import Oracle
Oracle.execute("""
CREATE OR REPLACE FUNCTION NUM_TO_REG(NUM IN NUMBER) RETURN VARCHAR2
  IS
  REG VARCHAR(6);
  X NUMBER;
  BEGIN
    X := NUM;
    REG := CHR(MOD(X, 26) + 97);
    X := FLOOR(X / 26);
    REG := REG || CHR(MOD(X, 10) + 48);
    X := FLOOR(X / 10);
    REG := REG || CHR(MOD(X, 10) + 48);
    X := FLOOR(X / 10);
    REG := REG || CHR(MOD(X, 10) + 48);
    X := FLOOR(X / 10);
    REG := REG || CHR(MOD(X, 26) + 97);
    X := FLOOR(X / 26);
    REG := REG || CHR(MOD(X, 26) + 97);
    RETURN (REG);
  END NUM_TO_REG;
""").close()

Oracle.execute("""
CREATE OR REPLACE PROCEDURE CHECK_REG_NUM(REG IN VARCHAR2)
  IS
    invalidRegNum EXCEPTION;
    X NUMBER;
  BEGIN
    X := ASCII(SUBSTR(REG, 6, 6));
    IF (X < 97) OR (122 < X) THEN
      RAISE invalidRegNum;
    END IF;

    X := ASCII(SUBSTR(REG, 5, 5));
    IF (X < 97) OR (122 < X) THEN
      RAISE invalidRegNum;
    END IF;

    X := ASCII(SUBSTR(REG, 4, 4));
    IF (X < 48) OR (57 < X) THEN
      RAISE invalidRegNum;
    END IF;

    X := ASCII(SUBSTR(REG, 3, 3));
    IF (X < 48) OR (57 < X) THEN
      RAISE invalidRegNum;
    END IF;

    X := ASCII(SUBSTR(REG, 2, 2));
    IF (X < 48) OR (57 < X) THEN
      RAISE invalidRegNum;
    END IF;

    X := ASCII(SUBSTR(REG, 1, 1));
    IF (X < 97) OR (122 < X) THEN
      RAISE invalidRegNum;
    END IF;

    EXCEPTION
    WHEN invalidRegNum THEN
      raise_application_error(-20100, 'Некорректный регистрационный номер');
  END;
""")

Oracle.execute("""
CREATE OR REPLACE FUNCTION REG_TO_NUM(REG IN VARCHAR2) RETURN NUMBER
  IS
    invalidRegNum EXCEPTION;
    N NUMBER;
    X NUMBER;
  BEGIN
    N := 0;

    CHECK_REG_NUM(REG);

    X := ASCII(SUBSTR(REG, 6, 6));
    N := N * 26;
    N := N + (X - 97);

    X := ASCII(SUBSTR(REG, 5, 5));
    N := N * 26;
    N := N + (X - 97);

    X := ASCII(SUBSTR(REG, 4, 4));
    N := N * 10;
    N := N + (X - 48);

    X := ASCII(SUBSTR(REG, 3, 3));
    N := N * 10;
    N := N + (X - 48);

    X := ASCII(SUBSTR(REG, 2, 2));
    N := N * 10;
    N := N + (X - 48);

    X := ASCII(SUBSTR(REG, 1, 1));
    N := N * 26;
    N := N + (X - 97);

    RETURN N;
    EXCEPTION
    WHEN invalidRegNum THEN
      raise_application_error(-20100, 'Некорректный регистрационный номер');
  END;
""")

Oracle.execute("""
CREATE OR REPLACE FUNCTION GET_REG_NUM RETURN VARCHAR2
  IS
  reg_val NUMBER;
  CURSOR interval IS
    SELECT * FROM FreeRegNum WHERE ROWNUM <= 1;
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