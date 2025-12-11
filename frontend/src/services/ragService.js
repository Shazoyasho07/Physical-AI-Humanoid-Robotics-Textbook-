/**
 * Service for interacting with the RAG API
 */

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

/**
 * Query the textbook content using RAG
 */
export const queryTextbook = async (textbookId, query, userId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/textbook/${textbookId}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        user_id: userId
      }),
    });

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error querying textbook:', error);
    throw error;
  }
};

/**
 * Create a RAG index for a textbook
 */
export const createRAGIndex = async (textbookId, embeddingModel = 'text-embedding-3-small') => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/rag-index`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        textbook_id: textbookId,
        embedding_model: embeddingModel
      }),
    });

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating RAG index:', error);
    throw error;
  }
};

/**
 * Get the status of a RAG index
 */
export const getRAGIndexStatus = async (textbookId) => {
  // Note: This would require a corresponding endpoint in the backend API
  // For now, we'll return a placeholder implementation
  console.warn('getRAGIndexStatus: API endpoint not yet implemented in backend');
  return { status: 'unknown' };
};