import requests
import logging

def upload_file_to_vk(vk, file_path, config):
    upload_url = vk.photos.getWallUploadServer(group_id=config['vk']['group_id'])['upload_url']
    files = {'photo': open(file_path, 'rb')}
    response = requests.post(upload_url, files=files).json()
    save_response = vk.photos.saveWallPhoto(group_id=config['vk']['group_id'], photo=response['photo'], server=response['server'], hash=response['hash'])[0]
    attachment = f"photo{save_response['owner_id']}_{save_response['id']}"
    logging.info(f'Файл загружен на сервер ВК: {attachment}')
    return attachment