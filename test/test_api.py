import json
import pytest
from app import create_app
from app.models import blog_storage, BlogPost

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestBlogAPI:
    def test_get_all_posts(self, client):
        """Test: Obtener todos los posts via API"""
        response = client.get('/api/posts')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'data' in data
        assert isinstance(data['data'], list)

    def test_create_post_valid(self, client):
        """Test: Crear post válido via API"""
        test_data = {
            'title': 'Test Post',
            'content': 'This is a test content',
            'author': 'Tester'
        }
        response = client.post('/api/posts', json=test_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['title'] == test_data['title']

    def test_create_post_invalid(self, client):
        """Test: Crear post inválido via API"""
        test_data = {'title': ''}  # Falta contenido
        response = client.post('/api/posts', json=test_data)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    def test_get_single_post(self, client):
        """Test: Obtener un post específico"""
        # Primero crear un post de prueba
        test_post = BlogPost(title='Test', content='Test content')
        created_post = blog_storage.create_post(test_post)
        
        response = client.get(f'/api/posts/{created_post.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['id'] == created_post.id

    def test_update_post(self, client):
        """Test: Actualizar un post existente"""
        test_post = BlogPost(title='Original', content='Original content')
        created_post = blog_storage.create_post(test_post)
        
        update_data = {'title': 'Updated', 'content': 'Updated content'}
        response = client.put(
            f'/api/posts/{created_post.id}',
            json=update_data
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['title'] == 'Updated'

    def test_delete_post(self, client):
        """Test: Eliminar un post"""
        test_post = BlogPost(title='To Delete', content='Delete me')
        created_post = blog_storage.create_post(test_post)
        
        response = client.delete(f'/api/posts/{created_post.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_search_posts(self, client):
        """Test: Buscar posts"""
        test_post = BlogPost(title='Search Test', content='Test content')
        blog_storage.create_post(test_post)
        
        response = client.get('/api/search?q=Search')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['count'] > 0
        assert 'Search' in data['data'][0]['title']

    def test_health_endpoint(self, client):
        """Test: Health check endpoint works"""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['version'] == '1.0.0'
        assert 'timestamp' in data
        assert data['tests_passing'] is True