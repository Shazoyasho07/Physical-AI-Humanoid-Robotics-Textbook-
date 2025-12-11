/**
 * Service for managing user preferences
 */

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

/**
 * Get user preferences for a specific textbook
 */
export const getUserPreferences = async (userId, textbookId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/${userId}/textbooks/${textbookId}/preferences`);
    
    if (!response.ok) {
      if (response.status === 404) {
        return null; // No preferences set yet
      }
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting user preferences:', error);
    throw error;
  }
};

/**
 * Set user preferences for a specific textbook
 */
export const setUserPreferences = async (userId, textbookId, selectedChapters) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/${userId}/textbooks/${textbookId}/preferences`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(selectedChapters),
    });
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error setting user preferences:', error);
    throw error;
  }
};

/**
 * Get filtered chapters based on user preferences
 */
export const getFilteredChapters = async (userId, textbookId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/users/${userId}/textbooks/${textbookId}/chapters`);
    
    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting filtered chapters:', error);
    throw error;
  }
};