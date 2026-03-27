CREATE DATABASE IF NOT EXISTS catalog_db;
USE catalog_db;

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    price FLOAT,
    weight FLOAT,
    category VARCHAR(50)
);

-- Anda menyuntikkan nominal harga dalam skala Rupiah
INSERT INTO products VALUES 
(1, 'Laptop', 15000000, 2, 'electronics'),
(2, 'Phone', 5000000, 1, 'electronics'),
(3, 'T-Shirt', 150000, 1, 'fashion'),
(4, 'Jeans', 250000, 2, 'fashion'),
(5, 'Coffee Maker', 800000, 3, 'appliances'),
(6, 'Blender', 600000, 4, 'appliances');