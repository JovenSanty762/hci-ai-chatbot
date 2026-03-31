-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS hci_chatbot;
USE hci_chatbot;

-- Tablas (SQLAlchemy se encarga de crearlas, pero esto es útil para Docker)
-- Puedes dejar esto vacío o usar solo para datos de prueba:

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
