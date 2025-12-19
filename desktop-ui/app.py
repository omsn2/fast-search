"""Flask API server for desktop UI."""
import sys
import os

# Add parent directory to path to find backend module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import subprocess
import platform
from backend.search.search_service import SearchService

app = Flask(__name__)
CORS(app)

# Initialize search service
search_service = SearchService(enable_watcher=False)


@app.route('/')
def index():
    """Serve the main UI."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Search for files."""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'results': []})
    
    results = search_service.search(query)
    
    # Convert SearchResult objects to dictionaries
    results_dict = [
        {
            'name': r.name,
            'path': r.path,
            'extension': r.extension,
            'modified_time': r.modified_time,
            'score': r.score
        }
        for r in results
    ]
    
    return jsonify({'results': results_dict})


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get index statistics."""
    stats = search_service.get_stats()
    return jsonify(stats)


@app.route('/api/open-file', methods=['POST'])
def open_file():
    """Open a file with default application."""
    data = request.json
    file_path = data.get('path', '')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File not found'})
    
    try:
        if platform.system() == 'Windows':
            os.startfile(file_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', file_path])
        else:  # Linux
            subprocess.run(['xdg-open', file_path])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    """Open file location in file explorer."""
    data = request.json
    file_path = data.get('path', '')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'success': False, 'error': 'File not found'})
    
    try:
        folder_path = os.path.dirname(file_path)
        
        if platform.system() == 'Windows':
            subprocess.run(['explorer', '/select,', file_path])
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', '-R', file_path])
        else:  # Linux
            subprocess.run(['xdg-open', folder_path])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/settings')
def settings_page():
    """Serve the settings page."""
    return render_template('settings.html')


@app.route('/api/settings/directories', methods=['GET'])
def get_directories():
    """Get list of indexed directories."""
    from backend.config.user_settings import UserSettings
    settings = UserSettings()
    return jsonify({'directories': settings.get_indexed_directories()})


@app.route('/api/settings/excluded', methods=['GET'])
def get_excluded():
    """Get list of excluded directories."""
    from backend.config.config import Config
    return jsonify({'excluded': sorted(list(Config.EXCLUDED_DIRS))})


@app.route('/api/settings/directories/add', methods=['POST'])
def add_directory():
    """Add a directory to index."""
    from backend.config.user_settings import UserSettings
    from backend.indexer.indexer import FileIndexer
    from backend.database.database import Database
    
    data = request.json
    directory = data.get('directory', '')
    
    if not directory:
        return jsonify({'success': False, 'error': 'No directory provided'})
    
    # Validate directory
    if not os.path.exists(directory):
        return jsonify({'success': False, 'error': 'Directory does not exist'})
    
    if not os.path.isdir(directory):
        return jsonify({'success': False, 'error': 'Path is not a directory'})
    
    # Add to settings
    settings = UserSettings()
    if not settings.add_directory(directory):
        return jsonify({'success': False, 'error': 'Failed to add directory'})
    
    # Index the directory
    try:
        indexer = FileIndexer()
        db = Database()
        
        total_indexed = 0
        for batch in indexer.index_directories([directory]):
            inserted = db.insert_files(batch)
            total_indexed += inserted
        
        db.close()
        
        # Reload search service
        search_service._load_index()
        
        return jsonify({'success': True, 'count': total_indexed})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/settings/directories/remove', methods=['POST'])
def remove_directory():
    """Remove a directory from index."""
    from backend.config.user_settings import UserSettings
    from backend.database.database import Database
    
    data = request.json
    directory = data.get('directory', '')
    
    if not directory:
        return jsonify({'success': False, 'error': 'No directory provided'})
    
    # Remove from settings
    settings = UserSettings()
    if not settings.remove_directory(directory):
        return jsonify({'success': False, 'error': 'Directory not in index'})
    
    # Remove files from database
    try:
        db = Database()
        # Delete all files from this directory
        cursor = db.conn.cursor()
        cursor.execute("DELETE FROM files WHERE path LIKE ?", (f"{directory}%",))
        db.conn.commit()
        deleted = cursor.rowcount
        db.close()
        
        # Reload search service
        search_service._load_index()
        
        return jsonify({'success': True, 'count': deleted})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/settings/reindex', methods=['POST'])
def reindex_all():
    """Reindex all configured directories."""
    from backend.config.user_settings import UserSettings
    from backend.indexer.indexer import FileIndexer
    from backend.database.database import Database
    
    settings = UserSettings()
    directories = settings.get_indexed_directories()
    
    if not directories:
        return jsonify({'success': False, 'error': 'No directories configured'})
    
    try:
        indexer = FileIndexer()
        db = Database()
        
        # Clear existing index
        db.clear_index()
        
        # Reindex all directories
        total_indexed = 0
        for batch in indexer.index_directories(directories):
            inserted = db.insert_files(batch)
            total_indexed += inserted
        
        db.close()
        
        # Reload search service
        search_service._load_index()
        
        return jsonify({'success': True, 'count': total_indexed})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/settings/autostart/status', methods=['GET'])
def get_autostart_status():
    """Get auto-start status."""
    try:
        from backend.utils.auto_start import AutoStart
        is_enabled = AutoStart.is_enabled()
        return jsonify({'enabled': is_enabled})
    except Exception as e:
        return jsonify({'enabled': False, 'error': str(e)})


@app.route('/api/settings/autostart/toggle', methods=['POST'])
def toggle_autostart():
    """Toggle auto-start on/off."""
    try:
        from backend.utils.auto_start import AutoStart
        success = AutoStart.toggle()
        is_enabled = AutoStart.is_enabled()
        return jsonify({'success': success, 'enabled': is_enabled})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def run_server(port=5000, debug=False):
    """Run the Flask server."""
    app.run(host='127.0.0.1', port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
