"""
Textbook generation script that creates Docusaurus structure from database content
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend src to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from backend.src.models.database import Textbook, Chapter
from backend.src.db.session import SessionLocal
from backend.src.config import settings


def generate_textbook_from_db(textbook_id: str, output_dir: str = "./docs"):
    """
    Generate Docusaurus markdown files from textbook content in the database
    """
    db = SessionLocal()
    try:
        # Fetch the textbook and its chapters from the database
        textbook = db.query(Textbook).filter(Textbook.id == textbook_id).first()
        if not textbook:
            print(f"Error: Textbook with ID {textbook_id} not found")
            return False
        
        chapters = db.query(Chapter).filter(
            Chapter.textbook_id == textbook_id
        ).order_by(Chapter.chapter_number).all()
        
        if not chapters:
            print(f"Warning: Textbook {textbook_id} has no chapters")
            return True
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the mapping from chapter titles to file names
        title_to_filename = {
            "Introduction to Physical AI": "intro",
            "Basics of Humanoid Robotics": "basics", 
            "ROS 2 Fundamentals": "ros2",
            "Digital Twin Simulation (Gazebo + Isaac)": "simulation",
            "Vision-Language-Action Systems": "vla",
            "Capstone: Simple AI-Robot Pipeline": "capstone"
        }
        
        # Generate a markdown file for each chapter
        for i, chapter in enumerate(chapters):
            # Determine the filename based on the chapter title or use a default
            filename = title_to_filename.get(chapter.title, f"chapter_{chapter.chapter_number:02d}")
            
            # Add frontmatter for Docusaurus with sidebar position
            frontmatter = f"""---
sidebar_position: {chapter.chapter_number}
---

# {chapter.title}

"""
            
            # Write the content to a markdown file
            file_path = os.path.join(output_dir, f"{filename}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter)
                f.write(chapter.content)
                
            print(f"Generated: {file_path}")
        
        # Update the sidebar configuration if needed (this is typically done manually once)
        print(f"Textbook generation completed for '{textbook.title}' ({len(chapters)} chapters)")
        return True
        
    except Exception as e:
        print(f"Error generating textbook: {str(e)}")
        return False
    finally:
        db.close()


def generate_all_textbooks(output_dir: str = "./docs"):
    """
    Generate Docusaurus markdown files for all textbooks in the database
    """
    db = SessionLocal()
    try:
        textbooks = db.query(Textbook).all()
        for textbook in textbooks:
            print(f"Generating textbook: {textbook.title} (ID: {textbook.id})")
            generate_textbook_from_db(textbook.id, output_dir)
        return True
    except Exception as e:
        print(f"Error generating all textbooks: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Example usage:
    # generate_textbook_from_db("some-textbook-id")
    # or
    # generate_all_textbooks()
    
    print("Textbook generation script - Run generate_textbook_from_db() or generate_all_textbooks() with appropriate parameters")