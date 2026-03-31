import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = '/api';   // gracias al nginx

function App() {
  const [step, setStep] = useState(0);
  const [patient, setPatient] = useState({ cedula: '', nombre_completo: '', telefono: '', email: '' });
  const [specialties, setSpecialties] = useState([]);
  const [selectedSpecialty, setSelectedSpecialty] = useState(null);
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [availabilities, setAvailabilities] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);

  // Cargar especialidades al inicio
  useEffect(() => {
    axios.get(`${API_BASE}/doctors/specialties/`).then(res => setSpecialties(res.data));
  }, []);

  const handlePatientSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post(`${API_BASE}/patients/`, patient);
    setPatient({ ...patient, id: res.data.id });
    setStep(2);
  };

  const handleSpecialtySelect = (spec) => {
    setSelectedSpecialty(spec);
    axios.get(`${API_BASE}/doctors/?specialty_id=${spec.id}`).then(res => {
      setDoctors(res.data);
      setStep(3);
    });
  };

  const handleDoctorSelect = async (doc) => {
    setSelectedDoctor(doc);
    setStep(4);   // Cambiamos a "Cargando horarios..."

    try {
      const res = await axios.get(`${API_BASE}/doctors/${doc.id}/availability`);
    
      // Convertimos los horarios a un formato más amigable para mostrar
      const formattedSlots = res.data.map(slot => ({
        id: slot.id,
        day_of_week: slot.day_of_week,
        day_name: getDayName(slot.day_of_week),
        start_time: slot.start_time,
        end_time: slot.end_time,
        // Generamos algunos horarios sugeridos dentro del rango (puedes mejorar esto)
        suggested_times: generateSuggestedTimes(slot.start_time, slot.end_time)
      }));

      setAvailabilities(formattedSlots);
    } catch (error) {
      alert("Este médico no tiene horarios configurados todavía.");
      setAvailabilities([]);
      }
  };

  // Funciones auxiliares
  const getDayName = (day) => {
  const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    return days[day];
  };

  const generateSuggestedTimes = (start, end) => {
    // Por simplicidad devolvemos el rango completo. Puedes mejorarlo para generar slots cada 30 min.
    return [`${start} - ${end}`];
  };

  const handleBooking = async () => {
    if (!selectedDoctor || !selectedSlot || !patient.id) {
      alert("Faltan datos para agendar la cita");
      return;
    }

    try {
      const appointmentData = {
        patient_id: patient.id,
        doctor_id: selectedDoctor.id,
        appointment_date: new Date().toISOString().split('T')[0], // Hoy por defecto (puedes mejorar con selector de fecha)
        start_time: selectedSlot.start_time || "09:00:00",
        end_time: selectedSlot.end_time || "10:00:00",
        notes: `Cita agendada desde el chatbot`
      };

      const response = await axios.post(`${API_BASE}/appointments/`, appointmentData);
    
      alert(`✅ ¡Cita agendada exitosamente!\n\nID de cita: ${response.data.id}`);
    
      // Reiniciar el flujo
      setStep(0);
      setPatient({ cedula: '', nombre_completo: '', telefono: '', email: '' });
      setSelectedSpecialty(null);
      setSelectedDoctor(null);
      setAvailabilities([]);
      setSelectedSlot(null);

    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Error al agendar la cita. Inténtalo nuevamente.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-3xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="bg-indigo-600 text-white p-6 text-center">
          <h1 className="text-3xl font-bold">🏥 HCI Chatbot Médico</h1>
          <p className="text-indigo-200 mt-1">Agendamiento inteligente de citas</p>
        </div>

        <div className="p-8">
          {step === 0 && (
            <div className="text-center">
              <h2 className="text-4xl font-semibold text-gray-800 mb-4">¡Bienvenido/a!</h2>
              <p className="text-xl text-gray-600 mb-8">Vamos a agendar tu cita médica en segundos</p>
              <button
                onClick={() => setStep(1)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-xl px-10 py-4 rounded-2xl transition"
              >
                Comenzar
              </button>
            </div>
          )}

          {step === 1 && (
            <form onSubmit={handlePatientSubmit} className="space-y-6">
              <h3 className="text-2xl font-medium">Tus datos</h3>
              <input type="text" placeholder="Cédula" value={patient.cedula} onChange={e => setPatient({...patient, cedula: e.target.value})} className="w-full p-4 border rounded-2xl" required />
              <input type="text" placeholder="Nombre completo" value={patient.nombre_completo} onChange={e => setPatient({...patient, nombre_completo: e.target.value})} className="w-full p-4 border rounded-2xl" required />
              <input type="tel" placeholder="Teléfono" value={patient.telefono} onChange={e => setPatient({...patient, telefono: e.target.value})} className="w-full p-4 border rounded-2xl" required />
              <input type="email" placeholder="Email (opcional)" value={patient.email} onChange={e => setPatient({...patient, email: e.target.value})} className="w-full p-4 border rounded-2xl" />
              <button type="submit" className="w-full bg-indigo-600 text-white py-4 rounded-2xl text-xl">Continuar →</button>
            </form>
          )}

          {step === 2 && (
            <div>
              <h3 className="text-2xl mb-6">¿Qué especialidad necesitas?</h3>
              <div className="grid grid-cols-2 gap-4">
                {specialties.map(spec => (
                  <button
                    key={spec.id}
                    onClick={() => handleSpecialtySelect(spec)}
                    className="p-6 border-2 hover:border-indigo-600 rounded-3xl text-left transition"
                  >
                    <div className="font-semibold">{spec.nombre}</div>
                    <div className="text-sm text-gray-500">{spec.descripcion}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h3 className="text-2xl mb-6">Médicos disponibles en {selectedSpecialty?.nombre}</h3>
              <div className="space-y-4">
                {doctors.map(doc => (
                  <button
                    key={doc.id}
                    onClick={() => handleDoctorSelect(doc)}
                    className="w-full p-6 border-2 hover:border-indigo-600 rounded-3xl text-left"
                  >
                    <div className="font-semibold text-lg">{doc.nombre_completo}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 4 && (
            <div>
              <h3 className="text-2xl mb-6">Horarios disponibles</h3>
              <div className="grid grid-cols-3 gap-4">
                {availabilities.map((slot, i) => (
                  <button
                    key={i}
                    onClick={() => handleSlotSelect(slot)}
                    className="p-6 border-2 hover:border-indigo-600 rounded-3xl text-center"
                  >
                    <div className="font-medium">{slot.day}</div>
                    <div className="text-2xl font-bold text-indigo-600">{slot.time}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 5 && (
            <div className="text-center">
              <h3 className="text-3xl font-semibold mb-8">¡Confirmación final!</h3>
              <div className="bg-gray-50 p-8 rounded-3xl mb-8 text-left">
                <p><strong>Paciente:</strong> {patient.nombre_completo}</p>
                <p><strong>Médico:</strong> {selectedDoctor.nombre_completo}</p>
                <p><strong>Horario:</strong> {selectedSlot.day} {selectedSlot.time}</p>
              </div>
              <button
                onClick={handleBooking}
                className="bg-green-600 hover:bg-green-700 text-white text-2xl px-16 py-6 rounded-3xl"
              >
                ✅ Agendar cita
              </button>
            </div>
          )}
        </div>

        {/* Progress bar */}
        <div className="h-2 bg-gray-100">
          <div className="h-2 bg-indigo-600 transition-all" style={{ width: `${(step + 1) * 20}%` }}></div>
        </div>
      </div>
    </div>
  );
}

export default App;
