# book_library

### setup
     docker build https://github.com/Esteban108/book_library.git
     
     docker run  --name book-library -p 8000:8000 book_library
     docker start  book-library
     docker exec -it book-library python manage.py createsuperuser --username=admin --email=admin@admin.com
     
     http://localhost:8000