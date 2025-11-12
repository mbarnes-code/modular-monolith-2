"""
Basic tests for the MTG Commander Map Service
"""
import os


def test_project_structure():
    """Test that the project structure is correct"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Check that key files exist
    assert os.path.exists(os.path.join(project_root, 'requirements.txt'))
    assert os.path.exists(os.path.join(project_root, 'make-map.sh'))
    assert os.path.exists(os.path.join(project_root, 'commander-map.ipynb'))
    assert os.path.exists(os.path.join(project_root, 'duplicates.txt'))
    edhrec_file = os.path.join(project_root, 'edhrec-to-scryfall.json')
    assert os.path.exists(edhrec_file)

    # Check that src/scripts directory exists and has key files
    scripts_dir = os.path.join(project_root, 'src', 'scripts')
    assert os.path.exists(scripts_dir)
    assert os.path.exists(os.path.join(scripts_dir, 'preprocess_data.py'))
    assert os.path.exists(os.path.join(scripts_dir, 'card.py'))
    assert os.path.exists(os.path.join(scripts_dir, 'calculate.py'))


def test_requirements_file_exists():
    """Test that requirements.txt exists and is not empty"""
    project_root = os.path.dirname(os.path.dirname(__file__))
    req_file = os.path.join(project_root, 'requirements.txt')
    
    assert os.path.exists(req_file)
    
    with open(req_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        assert len(content) > 0
        assert 'numpy' in content  # Should have numpy dependency
