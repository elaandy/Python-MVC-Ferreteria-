CREATE TABLE Productos (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
)
use pegratriplexsas

CREATE TABLE Ventas (
    id_venta INT IDENTITY(1,1) PRIMARY KEY,
    fecha DATETIME DEFAULT GETDATE(),
    total DECIMAL(10,2)
)

CREATE TABLE Detalle_Venta (
    id_detalle INT IDENTITY(1,1) PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
)

INSERT INTO Productos (nombre, categoria, precio, stock)
VALUES
('Martillo', 'Herramientas', 25000, 10),
('Destornillador', 'Herramientas', 12000, 20),
('Clavos 2 pulgadas', 'Fijaciones', 5000, 100);

SELECT v.id_venta, v.fecha, p.nombre, d.cantidad, d.precio_unitario
FROM Ventas v
JOIN Detalle_Venta d ON v.id_venta = d.id_venta
JOIN Productos p ON d.id_producto = p.id_producto;

SELECT * FROM Productos;


CREATE PROCEDURE RegistrarVenta
    @id_producto INT,
    @cantidad INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @precio DECIMAL(10,2);
    DECLARE @total DECIMAL(10,2);
    DECLARE @id_venta INT;

    -- Ver precio del producto
    SELECT @precio = precio
    FROM Productos
    WHERE id_producto = @id_producto;

    -- Verificar stock
    IF (SELECT stock FROM Productos WHERE id_producto = @id_producto) < @cantidad
    BEGIN
        RAISERROR ('Stock insuficiente', 16, 1);
        RETURN;
    END

    -- Crear venta
    INSERT INTO Ventas (total)
    VALUES (0);

    SET @id_venta = SCOPE_IDENTITY();

    -- Insertar detalle
    INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario)
    VALUES (@id_venta, @id_producto, @cantidad, @precio);

    -- Calcular total
    SET @total = @precio * @cantidad;

    UPDATE Ventas
    SET total = @total
    WHERE id_venta = @id_venta;

    -- Descontar stock
    UPDATE Productos
    SET stock = stock - @cantidad
    WHERE id_producto = @id_producto;

END;

EXEC RegistrarVenta @id_producto = 1, @cantidad = 2;