import json
import base64
import requests
from os.path import join
from typing import List, Dict

HOST = 'http://192.168.31.240:7861'
MODEL = 'cuteyukimixAdorable_echodimension'
DRAW_OPTIONS = {
    "prompt": "",
    "negative_prompt": "",
    "seed": -1,
    "subseed": -1,
    "subseed_strength": 0,
    "seed_resize_from_h": -1,
    'sampler_index': 'DPM++ 2M Karras',
    "seed_resize_from_w": -1,
    "batch_size": 1,
    "n_iter": 1,
    "steps": 20,
    "cfg_scale": 7,
    "width": 1080,
    "height": 720,
    "restore_faces": True,
    "do_not_save_samples": False,
    "do_not_save_grid": False,
    "eta": 0,
    "denoising_strength": 0,
    "s_min_uncond": 0,
    "s_churn": 0,
    "s_tmax": 0,
    "s_tmin": 0,
    "s_noise": 0,
    "override_settings": {},
    "override_settings_restore_afterwards": True,
    "refiner_switch_at": 0,
    "disable_extra_networks": False,
    "comments": {},
    "enable_hr": False,
    "firstphase_width": 0,
    "firstphase_height": 0,
    "hr_scale": 2,
    "hr_second_pass_steps": 0,
    "hr_resize_x": 0,
    "hr_resize_y": 0,
    "hr_prompt": "",
    "hr_negative_prompt": "",
    "script_args": [],
    "send_images": True,
    "save_images": False,
    "alwayson_scripts": {}
}

def darw_image(data: dict) -> str:
    url = join(HOST, 'sdapi/v1/txt2img')
    response = requests.post(url, data=json.dumps(data))
    return response.json()['images'][0]

def get_models() -> List[str]:
    url = join(HOST, 'sdapi/v1/sd-models')
    response = requests.get(url)
    return response.json()

def set_model(model_title: str) -> str:
    url = join(HOST, 'sdapi/v1/options')
    response = requests.post(url, data=json.dumps({
        'sd_model_checkpoint': model_title
    }))
    return response.json()

def save_image(image: str, filename: str) -> str:
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(image))

def draw_image_api(prompt: str) -> bytes:
    '''
    return image bytes
    '''
    cuteyuki = None

    models = get_models()
    for model in models:
        if model['model_name'] == MODEL:
            cuteyuki = model
            break
    
    if cuteyuki is None:
        raise Exception('model not found')
    
    set_model(cuteyuki['title'])
    DRAW_OPTIONS['prompt'] = prompt
    image = darw_image(DRAW_OPTIONS)

    return base64.b64decode(image)

if __name__ == '__main__':
    cuteyuki = None

    models = get_models()
    for model in models:
        if model['model_name'] == MODEL:
            cuteyuki = model
            break
    
    if cuteyuki is None:
        raise Exception('model not found')
    
    set_model(cuteyuki['title'])
    DRAW_OPTIONS['prompt'] = 'girl，full-body，white stocking，inside，window，high light in hair，white hair'
    
    image = darw_image(DRAW_OPTIONS)
    save_image(image, 'images/cuteyuki.png')