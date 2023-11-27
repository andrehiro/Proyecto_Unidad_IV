use tienda;
SELECT * FROM users;
delete from users where id = 8;
CREATE TABLE users (
 id smallint unsigned NOT NULL ,
 username varchar(20) NOT NULL,
 password char(102) NOT NULL,
 fullname varchar(50),
 usertype tinyint NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE productos (
 id smallint unsigned NOT NULL AUTO_INCREMENT,
 nombre varchar(50) NOT NULL,
 imagen varchar(255) NOT NULL,
 precio decimal(10,2) NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER //
CREATE PROCEDURE sp_AddProduct(
    IN pNombre VARCHAR(50),
    IN pImagen VARCHAR(255),
    IN pPrecio DECIMAL(10, 2)
)
BEGIN
    DECLARE nueva_id SMALLINT UNSIGNED;

    SELECT COALESCE(MIN(t.id) + 1, 1) INTO nueva_id
    FROM (
        SELECT id FROM productos
        UNION
        SELECT 0 AS id
    ) t
    WHERE NOT EXISTS (
        SELECT 1 FROM productos WHERE id = t.id + 1
    );

    SET @sql = CONCAT('ALTER TABLE productos AUTO_INCREMENT=', nueva_id);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    INSERT INTO productos (id, nombre, imagen, precio)
    VALUES (nueva_id, pNombre, pImagen, pPrecio);
END //

DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_AddUser(IN pUserName VARCHAR(20), IN pPassword VARCHAR(102), IN pFullName VARCHAR(50), IN pUserType tinyint)
BEGIN
    DECLARE nueva_id SMALLINT UNSIGNED;
    DECLARE hashedPassword VARCHAR(255);

    SELECT COALESCE(MIN(t.id) + 1, 1) INTO nueva_id
    FROM (
        SELECT id FROM users
        UNION
        SELECT 0 AS id
    ) t
    WHERE NOT EXISTS (
        SELECT 1 FROM users WHERE id = t.id + 1
    );

    SET @sql = CONCAT('ALTER TABLE users AUTO_INCREMENT=', nueva_id);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET hashedPassword = SHA2(pPassword, 256);

    INSERT INTO users (id, username, password, fullname, usertype)
    VALUES (nueva_id, pUserName, hashedPassword, pFullName, pUserType);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(IN pUsername VARCHAR(20), IN pPlainTextPassword VARCHAR(20))
BEGIN
 DECLARE storedPassword VARCHAR(255);

 SELECT password INTO storedPassword FROM users
 WHERE username = pUsername COLLATE utf8mb4_unicode_ci;

 IF storedPassword IS NOT NULL AND storedPassword = SHA2(pPlainTextPassword, 256) THEN
 SELECT id, username, storedPassword, fullname, usertype FROM users
 WHERE username = pUserName COLLATE utf8mb4_unicode_ci;
 ELSE
 SELECT NULL;
 END IF;
END //
DELIMITER ;

call sp_AddUser("admin","123","juan perez",1);
call sp_AddUser("andre","123","Andre Hidrogo",0);
call sp_AddUser("pierre","123","Pierre Hidrogo",0);
call sp_AddUser("u1","123","u1",0);
call sp_verifyIdentity("admin","123");

call sp_AddProduct("Creeper","https://http2.mlstatic.com/D_NQ_NP_975559-MLU69214214278_052023-O.webp","75");

DELETE FROM productos WHERE id =2;

SELECT * FROM productos;
SELECT * FROM users;