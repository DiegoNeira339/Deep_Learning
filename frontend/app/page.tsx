'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Camera, Loader2, UserCheck, AlertCircle } from 'lucide-react';

export default function ReconocimientoFacial() {
  const [imagen, setImagen] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [cargando, setCargando] = useState(false);
  const [resultado, setResultado] = useState<{ persona: string; probabilidad: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  // ==========================================
  // DICCIONARIO DE TRADUCCIÓN
  // ==========================================
  // Aquí traducimos la etiqueta fea de la carpeta al nombre real y bonito
  const nombresReales: Record<string, string> = {
    "grupo5_persona01": "Diego Neira",
    "grupo1_personaA": "Constanza Sánchez",
    "grupo2_personaB": "Demián González",
    // NOTA: Añade aquí a todos los demás cuando Demián te pase la lista de carpetas
  };

  const manejarImagen = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImagen(file);
      setPreview(URL.createObjectURL(file));
      setResultado(null);
      setError(null);
    }
  };

  const analizarImagen = async () => {
    if (!imagen) return;
    setCargando(true);
    setError(null);
    setResultado(null);

    // ==========================================
    // MODO SIMULADOR (Mientras llega el .keras)
    // ==========================================
    setTimeout(() => {
      // Esta es la etiqueta cruda que simulamos que devuelve la API
      const etiquetaCruda = "grupo5_persona01"; 

      setResultado({
        // Busca la etiqueta en el diccionario. Si no existe, muestra la etiqueta cruda por defecto
        persona: nombresReales[etiquetaCruda] || etiquetaCruda, 
        probabilidad: 98.5
      });
      setCargando(false);
    }, 2500);

    /* 
    // ==========================================
    // MODO REAL (Descomentar cuando Demián mande el modelo)
    // ==========================================
    const formData = new FormData();
    formData.append('file', imagen);
    try {
      const response = await fetch('http://localhost:5000/predecir', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (response.ok) {
        const etiquetaDetectada = data.persona_detectada;
        setResultado({ 
          persona: nombresReales[etiquetaDetectada] || etiquetaDetectada, 
          probabilidad: data.probabilidad 
        });
      } else {
        setError(data.error || 'Error al analizar la imagen.');
      }
    } catch (err) {
      setError('Error de conexión. Asegúrate de que Flask esté corriendo.');
    } finally {
      setCargando(false);
    }
    */
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4 font-sans">
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100 p-8"
      >
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2 }}
            className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 text-blue-600"
          >
            <Camera size={32} />
          </motion.div>
          <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">Escáner Facial</h1>
          <p className="text-slate-500 mt-2 text-sm">Sube una fotografía para que la Red Neuronal la identifique.</p>
        </div>

        {/* Caja de subida de imagen */}
        <div className="relative group">
          <div className={`border-2 border-dashed rounded-2xl p-2 transition-all duration-300 ease-in-out flex flex-col items-center justify-center min-h-[260px] cursor-pointer overflow-hidden
            ${preview ? 'border-blue-400 bg-blue-50' : 'border-slate-300 bg-slate-50 hover:bg-slate-100 hover:border-blue-300'}`}
          >
            <input 
              type="file" 
              accept="image/*" 
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              style={{ opacity: 0 }} // <- Aquí forzamos que el botón sea invisible
              onChange={manejarImagen}
            />
            
            <AnimatePresence mode="wait">
              {preview ? (
                <motion.img 
                  key="preview"
                  initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
                  src={preview} 
                  alt="Vista previa" 
                  className="w-full h-full object-cover rounded-xl shadow-sm" 
                />
              ) : (
                <motion.div key="placeholder" className="flex flex-col items-center text-slate-400 pointer-events-none">
                  <Upload className="w-10 h-10 mb-3 text-slate-300 group-hover:text-blue-400 transition-colors" />
                  <span className="font-semibold text-slate-600">Haz clic o arrastra tu foto</span>
                  <span className="text-xs mt-2 text-slate-400">Soporta JPG, PNG</span>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Botón Principal */}
        <button
          onClick={analizarImagen}
          disabled={!imagen || cargando}
          className="w-full mt-6 bg-slate-900 hover:bg-blue-600 disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold py-4 px-4 rounded-2xl transition-all duration-300 flex items-center justify-center gap-2 shadow-lg hover:shadow-blue-500/30 disabled:shadow-none"
        >
          {cargando ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Procesando con CNN...
            </>
          ) : (
            'Analizar Rostro'
          )}
        </button>

        {/* Tarjeta de Error */}
        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
              className="mt-4 p-4 bg-red-50 border border-red-100 text-red-600 rounded-2xl text-sm flex items-start gap-3"
            >
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <p>{error}</p>
            </motion.div>
          )}
        </AnimatePresence>

{/* Tarjeta de Resultado */}
        <AnimatePresence>
          {resultado && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
              className="mt-6 p-6 border-2 border-emerald-100 bg-emerald-50 rounded-2xl overflow-hidden relative"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-emerald-400"></div>
              <div className="flex items-center gap-3 mb-4 text-emerald-700">
                <div className="p-2 bg-emerald-100 rounded-full">
                  <UserCheck className="w-6 h-6" />
                </div>
                <h3 className="font-bold text-lg">Identidad Confirmada</h3>
              </div>
              
              <div className="bg-white p-4 rounded-xl shadow-sm border border-emerald-100/50">
                <p className="text-xs text-slate-400 uppercase font-bold tracking-wider mb-1">Sujeto Detectado</p>
                <p className="text-xl font-extrabold text-slate-800 mb-4">{resultado.persona}</p>
                
                <div className="flex justify-between items-end mb-2">
                  <span className="text-xs font-bold text-slate-500">Nivel de Confianza</span>
                  <span className="text-sm font-bold text-emerald-600">{resultado.probabilidad}%</span>
                </div>
                
                {/* Barra de progreso animada */}
                <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${resultado.probabilidad}%` }}
                    transition={{ duration: 1.2, ease: "easeOut", delay: 0.2 }}
                    className="bg-emerald-500 h-full rounded-full"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </motion.div>
    </div>
  );
}