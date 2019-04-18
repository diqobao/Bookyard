import urllib.request
from PIL import Image
from bookyardApp.db import get_db
from bookyardApp.models import updateImg

def check_book_img(image_url):
    try:
        image = Image.open(urllib.request.urlopen(image_url))
        width, height = image.size
        if width == 1:
           return False
    except:
        print('error')
        # image_url = 'https://cdn.pixabay.com/photo/2018/01/17/18/43/book-3088777_1280.png'
        return False
    return True

def update_img(books):
    db = get_db()
    changed = False
    for book in books:
        if check_book_img(book['img_url_l']) == False:
            updateImg(db, book['bookId'])
            changed = True
    return changed

