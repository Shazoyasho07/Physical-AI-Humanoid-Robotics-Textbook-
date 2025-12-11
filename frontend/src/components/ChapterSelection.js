/**
 * Chapter Selection Component
 * Allows users to select which chapters they want to focus on
 */
import React, { useState, useEffect } from 'react';
import './ChapterSelection.css';

const ChapterSelection = ({ textbookId, userId, onChapterSelection }) => {
  const [allChapters, setAllChapters] = useState([]);
  const [selectedChapters, setSelectedChapters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Fetch available chapters for this textbook
  useEffect(() => {
    const fetchChapters = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `${process.env.REACT_APP_API_BASE_URL}/api/v1/textbooks/${textbookId}/chapters`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch chapters');
        }
        
        const data = await response.json();
        setAllChapters(data.chapters);
      } catch (error) {
        console.error('Error fetching chapters:', error);
      } finally {
        setLoading(false);
      }
    };

    if (textbookId) {
      fetchChapters();
    }
  }, [textbookId]);

  // Fetch user's existing preferences
  useEffect(() => {
    const fetchUserPreferences = async () => {
      if (!userId || !textbookId) return;

      try {
        const response = await fetch(
          `${process.env.REACT_APP_API_BASE_URL}/api/v1/users/${userId}/textbooks/${textbookId}/preferences`
        );
        
        if (response.ok) {
          const data = await response.json();
          const savedChapterIds = JSON.parse(data.selected_chapters || '[]');
          setSelectedChapters(savedChapterIds);
        }
      } catch (error) {
        console.error('Error fetching user preferences:', error);
        // If there's an error, we'll just leave selectedChapters as empty
      }
    };

    fetchUserPreferences();
  }, [userId, textbookId]);

  const handleChapterToggle = (chapterId) => {
    setSelectedChapters(prev => 
      prev.includes(chapterId)
        ? prev.filter(id => id !== chapterId)
        : [...prev, chapterId]
    );
  };

  const handleSavePreferences = async () => {
    if (!userId) {
      alert('Please log in to save your preferences');
      return;
    }

    try {
      setSaving(true);
      
      const response = await fetch(
        `${process.env.REACT_APP_API_BASE_URL}/api/v1/users/${userId}/textbooks/${textbookId}/preferences`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(selectedChapters),
        }
      );

      if (!response.ok) {
        throw new Error('Failed to save preferences');
      }

      alert('Preferences saved successfully!');
      if (onChapterSelection) {
        onChapterSelection(selectedChapters);
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      alert('Error saving preferences. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="chapter-selection">Loading chapters...</div>;
  }

  return (
    <div className="chapter-selection">
      <h3>Select Your Focus Chapters</h3>
      <p>Choose the chapters you want to prioritize in your learning:</p>
      
      <div className="chapter-list">
        {allChapters.map((chapter) => (
          <div 
            key={chapter.id} 
            className={`chapter-item ${selectedChapters.includes(chapter.id) ? 'selected' : ''}`}
            onClick={() => handleChapterToggle(chapter.id)}
          >
            <input
              type="checkbox"
              checked={selectedChapters.includes(chapter.id)}
              onChange={() => {}} // Controlled by onClick
              className="chapter-checkbox"
            />
            <span className="chapter-title">
              {chapter.chapter_number}. {chapter.title}
            </span>
          </div>
        ))}
      </div>
      
      <button 
        onClick={handleSavePreferences} 
        disabled={saving}
        className="save-preferences-btn"
      >
        {saving ? 'Saving...' : 'Save Preferences'}
      </button>
    </div>
  );
};

export default ChapterSelection;