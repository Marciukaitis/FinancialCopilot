/** Preguntas sugeridas para demo del RAG y la memoria conversacional. */

export const SAMPLE_QUESTIONS = {
  prestamos: {
    title: "Sobre préstamos",
    questions: [
      "¿Cuál es el monto máximo de un préstamo?",
      "¿Cuáles son los plazos disponibles?",
      "¿Qué documentación necesita un cliente para solicitar un préstamo?",
      "¿Puede cancelar anticipadamente un préstamo?",
      "¿Qué sucede si un cliente entra en mora?",
      "¿Cuál es el porcentaje máximo de ingresos que puede representar una cuota?",
    ],
  },
  productos: {
    title: "Sobre productos",
    questions: [
      "¿Qué productos financieros ofrece la empresa?",
      "¿Cuál es la diferencia entre el préstamo personal y el préstamo premium?",
      "¿Qué cubre el seguro de protección de cuotas?",
      "¿Qué es una refinanciación?",
    ],
  },
  procedimientos: {
    title: "Sobre procedimientos",
    questions: [
      "¿Cómo es el proceso de alta de un cliente?",
      "¿Qué pasos siguen para otorgar un préstamo?",
      "¿Qué reportes genera el sistema?",
      "¿Quién puede eliminar registros?",
      "¿Qué políticas de seguridad existen?",
      "¿Cómo se registran las modificaciones de un cliente?",
    ],
  },
};

export const FOLLOWUP_FLOW = [
  "¿Cuál es el monto máximo?",
  "¿Y cuál es el plazo?",
  "¿Qué documentos necesito?",
  "¿Puedo cancelar antes?",
];

export const OUT_OF_SCOPE_QUESTIONS = [
  "¿Cuál es la tasa de interés?",
  "¿Cuál es el horario de atención?",
  "¿Quién es el gerente de la empresa?",
  "¿Cuántas sucursales tiene la financiera?",
  "¿Cuál fue la facturación del año pasado?",
];
