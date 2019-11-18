import os
import shutil   # https://www.jb51.net/article/145522.htm
import datetime
import random

from fastapi import APIRouter, File, UploadFile
from typing import List
from starlette.responses import HTMLResponse

router = APIRouter()


@router.post("/task/upload")
async def task_upload_files(files: List[UploadFile] = File(...)):
    allow_mime_type = ['image/jpeg', 'image/jpg', 'image/png']

    # 保存目录设置
    random_str_list = random.sample('zyxwvutsrqponmlkjihgfedcba9876543210', 32)
    random_path = ''.join(random_str_list)
    save_path = 'runtime/tinyimg/' + str(datetime.date.today().strftime('%y%m%d')) + '/' + random_path + '/'
    os.makedirs(save_path)
    zip_file_path = save_path + 'imgs'

    for upload_file in files:
        filename = upload_file.filename  # 文件名
        extension = os.path.splitext(upload_file.filename)[1]  # 扩展名
        # mime_type = upload_file.content_type   # mime 类型

        # 判断是否在允许的类型中
        if upload_file.content_type not in allow_mime_type :
            continue


        # create empty file to copy the file_object to
        upload_folder = open(os.path.join(save_path, upload_file.filename), 'wb+')
        shutil.copyfileobj(upload_file.file, upload_folder)
        upload_folder.close()

        # return {"filename": upload_file.filename}
    shutil.make_archive(zip_file_path, 'zip', save_path)
    return {"filenames": [file.filename for file in files]}


@router.get("/task/cron_delete_file")
async def cron_delete():
    return {"task": "cron_delete"}


@router.get("/test_upload")
async def main():
    content = """
        <body>
        <form action="/tinyimg/task/upload" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)