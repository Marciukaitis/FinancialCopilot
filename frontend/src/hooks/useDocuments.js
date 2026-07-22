import { useCallback, useEffect, useState } from "react";
import { getIndexStatus, uploadDocument } from "../api/client";

const EMPTY_STATUS = {
  documents_count: 0,
  chunks_indexed: 0,
  collection_name: "finance_documents",
  documents: [],
  embedding_model: "",
  llm_model: "",
  vector_db: "ChromaDB",
  indexed: false,
  status: "unknown",
};

export function useDocuments() {
  const [status, setStatus] = useState(EMPTY_STATUS);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [lastUploaded, setLastUploaded] = useState("");

  const refreshStatus = useCallback(async () => {
    try {
      const data = await getIndexStatus();
      setStatus({ ...EMPTY_STATUS, ...data });
      setError("");
    } catch (err) {
      setError(err.message || "No se pudo obtener el estado de indexación");
    }
  }, []);

  useEffect(() => {
    refreshStatus();
  }, [refreshStatus]);

  const upload = useCallback(
    async (file) => {
      if (!file || uploading) return;

      setUploading(true);
      setError("");

      try {
        const result = await uploadDocument(file);
        setLastUploaded(result.filename);
        await refreshStatus();
      } catch (err) {
        setError(err.message || "Error al subir el documento");
        throw err;
      } finally {
        setUploading(false);
      }
    },
    [refreshStatus, uploading],
  );

  return {
    status,
    uploading,
    error,
    lastUploaded,
    upload,
    refreshStatus,
  };
}
