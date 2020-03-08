# book_library

### setup
     git clone  https://github.com/Esteban108/book_library.git
     cd book_library
     docker build  -t book_library . 
     
     docker run  --name book-library -p 8000:8000 book_library
     docker start  book-library
     docker exec -it book-library python manage.py createsuperuser --username=admin --email=admin@admin.com
     
     http://localhost:8000