CREATE TABLE IF NOT EXISTS specialties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO specialties (name) VALUES 
('Medicina General'),
('Pediatría'),
('Cardiología'),
('Ginecología'),
('Ortopedia'),
('Dermatología'),
('Oftalmología'),
('Cirugía General'),
('Psicología'),
('Neurología');

CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(50) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    conversation_id VARCHAR(100) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
