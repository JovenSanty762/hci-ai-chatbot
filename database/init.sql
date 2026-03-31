-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS hci_chatbot;

-- Tablas (SQLAlchemy se encarga de crearlas, pero esto es útil para Docker)
-- Puedes dejar esto vacío o usar solo para datos de prueba:

-- =============================================
-- Base de datos para Chatbot de Agendamiento Médico
-- =============================================

USE hci_chatbot;

-- =============================================
-- Tablas principales
-- =============================================

-- Especialidades médicas
CREATE TABLE IF NOT EXISTS specialties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) UNIQUE NOT NULL,
    descripcion VARCHAR(255) NULL
);

-- Médicos
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(120) NOT NULL,
    specialty_id INT NOT NULL,
    telefono VARCHAR(15) NULL,
    licencia VARCHAR(30) UNIQUE NULL,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (specialty_id) REFERENCES specialties(id) ON DELETE CASCADE
);

-- Horarios de disponibilidad de médicos
CREATE TABLE IF NOT EXISTS doctor_availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    day_of_week TINYINT NOT NULL,           -- 0 = Lunes, 1 = Martes, ..., 6 = Domingo
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- Pacientes (registro desde el chatbot)
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre_completo VARCHAR(120) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE NULL,
    fecha_nacimiento DATE NULL,
    genero ENUM('masculino', 'femenino', 'otro') NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Citas agendadas
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status ENUM('pendiente', 'confirmada', 'cancelada', 'completada') DEFAULT 'pendiente',
    notes TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- =============================================
-- Datos de prueba (Seed)
-- =============================================

INSERT INTO specialties (nombre, descripcion) VALUES
    ('Medicina General', 'Consulta general')
    ('Cardiología', 'Especialidad del corazón'),
    ('Pediatría', 'Niños y adolescentes'),
    ('Ginecología y obstetricia', 'Salud femenina'),
    ('Dermatología', 'Piel y enfermedades cutáneas'),
    ('Cardiología pediatrica', 'Especialidad del corazón infantil'),
    ('Cirugia general', 'Procedimientos quirurgicos generales'),
    ('Cirugia maxilofacial', 'Procedimientos quirurgicos faciales'),
    ('Dolor y cuidados paliativos', 'Evaluacion y cuidado del dolor agudo'),
    ('Gastroenterologia', 'Cuidados del sistema digestivo'),
    ('Anestesiologia', 'Cuidado integral Post-Quirurgico'),
    ('Nefrologia', 'Enfermedades renales'),
    ('Neurocirugia', 'Procedimiento quirurgico del sistema nervioso central'),
    ('Nutricion', 'Cuidado de la relacion entre alimentacion y el cuerpo'),
    ('Oftalmologia', 'Cuidado y tratamiento de enfermedades oculares'),
    ('Ortopedia y traumatologia', 'tratamiento del sistema musculoesqueletico'),
    ('Perinatologia', 'Manejo de embarazos de alto riesgo'),
    ('Psicologia', 'Diagnostico de la conducta humana'),
    ('Reumatologia', 'Tratamiento del aparato locomotor'),
    ('Urologia', 'Enfermedades del sistema urinario');

-- Datos de prueba de médicos
INSERT INTO doctors (nombre_completo, specialty_id, telefono, licencia, is_active) VALUES
    ('Dr. Juan Pérez', 1, '3101234567', '123456', true),
    ('Dra. María López', 2, '3107654321', '654321', true),
    ('Dr. Carlos Ruiz', 5, '3109876543', '987654', true);

-- Horarios de ejemplo (lunes = 0, martes = 1, etc.)
INSERT INTO doctor_availability (doctor_id, day_of_week, start_time, end_time) VALUES
    (1, 0, '08:00:00', '12:00:00'),  -- Dr. Pérez lunes mañana
    (1, 0, '14:00:00', '18:00:00'),  -- Dr. Pérez lunes tarde
    (2, 1, '09:00:00', '13:00:00');  -- Dra. López martes mañana
