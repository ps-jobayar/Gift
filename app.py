import os
import sys
import json
import base64
import asyncio
import aiohttp
import requests
import urllib3
import binascii
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.json_format import MessageToDict, MessageToJson
from google.protobuf.message import DecodeError

# --- Protobuf Dependencies ---
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

# --- Additional Protobuf Imports ---
import like_pb2
import like_count_pb2
import uid_generator_pb2

# Compile/Register Protobuf Descriptors Inline
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MajorLoginReq_pb2', _globals)

DESCRIPTOR2 = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3')
_globals2 = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR2, _globals2)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR2, 'MajorLoginRes_pb2', _globals2)

MajorLogin = _globals['MajorLogin']
MajorLoginRes = _globals2['MajorLoginRes']

# Compiled Gift Engine Protocol Buffers
import GetGiftStoreDetails_pb2
import GetWallet_pb2
import SendGift_pb2

# --- App Config ---
load_dotenv()
IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# --- SECURE MASTER CRYPTO CONFIG ---
CORE_CIPHER_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
CORE_CIPHER_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
CLIENT_AGENT_SPOOF = "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"

CATEGORY_MAP_PRO = {
    "902": "Avatar Frame", "214": "Face Paint", "101": "Female Core Skills", "102": "Male Core Skills", 
    "103": "Microchips", "905": "Parachutes", "710": "Premium Bundles", "720": "Super Bundles", 
    "203": "Jackets/Tops", "204": "Pants/Bottoms", "205": "Sneakers/Shoes", "211": "Head/Hairs", "901": "Banners", 
    "131": "Pet Evolution", "130": "Pet Emotes", "903": "Loot Boxes", "904": "Tactical Backpacks", 
    "906": "Skyboards", "907": "Exotic Others", "908": "Super Vehicles", "909": "Vip Emotes", 
    "911": "SkyWings Flight", "922": "Skill Weapon Skins",
}

ZIBON_SYSTEM_CACHE = {}

# --- Helper Functions ---
def perform_aes_injection(payload_bytes):
    cipher_engine = AES.new(CORE_CIPHER_KEY, AES.MODE_CBC, CORE_CIPHER_IV)
    return cipher_engine.encrypt(pad(payload_bytes, AES.block_size))

def encrypt_message(plaintext):
    try:
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(plaintext, AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        return binascii.hexlify(encrypted_message).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Error encrypting message: {e}")
        return None

def fetch_regional_endpoint(region_id):
    if region_id == "IND": return "https://client.ind.freefiremobile.com"
    elif region_id in ["BR", "US", "SAC", "NA"]: return "https://client.us.freefiremobile.com"
    return "https://clientbp.ggpolarbear.com"

def extract_jwt_payload(token_string):
    try:
        segment = token_string.split('.')[1]
        segment += '=' * (4 - len(segment) % 4)
        parsed_json = json.loads(base64.b64decode(segment))
        return parsed_json.get("lock_region"), parsed_json.get("external_id")
    except Exception: return None, None

def decode_jwt_full(token: str) -> dict:
    parts = token.split('.')
    if len(parts) != 3: return {}
    try:
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '==').decode())
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode())
        return {"header": header, "payload": payload}
    except Exception: return {}

def build_major_login(open_id: str, access_token: str, platform_type: int) -> bytes:
    major = MajorLogin()
    major.event_time = "2025-03-23 12:00:00"
    major.game_name = "free fire"
    major.platform_id = 1
    major.client_version = "1.123.1"
    major.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major.system_hardware = "Handheld"
    major.telecom_operator = "Verizon"
    major.network_type = "WIFI"
    major.screen_width = 1920
    major.screen_height = 1080
    major.screen_dpi = "280"
    major.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major.memory = 3003
    major.gpu_renderer = "Adreno (TM) 640"
    major.gpu_version = "OpenGL ES 3.1 v1.46"
    major.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major.client_ip = "223.191.51.89"
    major.language = "en"
    major.open_id = open_id
    major.open_id_type = "4"
    major.device_type = "Handheld"
    major.memory_available.version = 55
    major.memory_available.hidden_value = 81
    major.access_token = access_token
    major.platform_sdk_id = 1
    major.network_operator_a = "Verizon"
    major.network_type_a = "WIFI"
    major.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major.external_storage_total = 36235
    major.external_storage_available = 31335
    major.internal_storage_total = 2519
    major.internal_storage_available = 703
    major.game_disk_storage_available = 25010
    major.game_disk_storage_total = 26628
    major.external_sdcard_avail_storage = 32992
    major.external_sdcard_total_storage = 36235
    major.login_by = 3
    major.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major.reg_avatar = 1
    major.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major.channel_type = 3
    major.cpu_type = 2
    major.cpu_architecture = "64"
    major.client_version_code = "2019118695"
    major.graphics_api = "OpenGLES2"
    major.supported_astc_bitset = 16383
    major.login_open_id_type = 4
    major.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major.loading_time = 13564
    major.release_channel = "android"
    major.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major.android_engine_init_flag = 110009
    major.if_push = 1
    major.is_vpn = 1
    major.origin_platform_type = str(platform_type)
    major.primary_platform_type = str(platform_type)
    return major.SerializeToString()

def try_major_login(open_id: str, access_token: str, platform_type: int):
    payload = build_major_login(open_id, access_token, platform_type)
    encrypted_payload = perform_aes_injection(payload)
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB53"
    }
    try:
        resp = requests.post(url, data=encrypted_payload, headers=headers, verify=False, timeout=10)
        if resp.status_code != 200: return None
        major_res = MajorLoginRes()
        major_res.ParseFromString(resp.content)
        if major_res.token:
            return {
                "account_uid": str(major_res.account_uid),
                "region": major_res.region,
                "token": major_res.token,
                "url": major_res.url,
                "timestamp": major_res.timestamp,
                "key": major_res.key.hex(),
                "iv": major_res.iv.hex()
            }
    except Exception as e:
        print(f"MajorLogin error for platform {platform_type}: {e}")
    return None

def dispatch_wallet_query(jwt, login_token, region):
    req_structure = GetWallet_pb2.CSGetWalletReq(login_token=login_token, topup_rebate=False)
    api_headers = {
        "Authorization": f"Bearer {jwt}", "X-GA": "v1 1", "ReleaseVersion": "OB53", 
        "Content-Type": "application/octet-stream", "User-Agent": CLIENT_AGENT_SPOOF
    }
    try:
        endpoint = f"{fetch_regional_endpoint(region)}/GetWallet"
        encrypted_body = perform_aes_injection(req_structure.SerializeToString())
        res = requests.post(endpoint, data=encrypted_body, headers=api_headers, verify=False, timeout=10)
        if res.status_code == 200:
            wallet_pb = GetWallet_pb2.CSGetWalletRes()
            wallet_pb.ParseFromString(res.content)
            w_data = wallet_pb.wallet
            formatted_time = datetime.fromtimestamp(w_data.last_topup_time).strftime('%d %b %Y, %I:%M %p') if w_data.last_topup_time > 0 else "Never"
            return {"gold": w_data.coins, "diamond": w_data.gems, "last_topup": formatted_time}
    except Exception: pass
    return {"gold": 0, "diamond": 0, "last_topup": "SYNC_FAILED"}

# --- Like System Functions ---
def load_tokens(server_name):
    try:
        if server_name == "IND":
            with open("token_ind.json", "r") as f:
                tokens = json.load(f)
        elif server_name in {"BR", "US", "SAC", "NA"}:
            with open("token_br.json", "r") as f:
                tokens = json.load(f)
        else:
            with open("token_bd.json", "r") as f:
                tokens = json.load(f)
        return tokens
    except Exception as e:
        app.logger.error(f"Error loading tokens for server {server_name}: {e}")
        return None

def create_protobuf_message(user_id, region):
    try:
        message = like_pb2.like()
        message.uid = int(user_id)
        message.region = region
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error create_protobuf_message: {e}")
        return None

async def send_request(encrypted_uid, token, url):
    try:
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB53"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers) as response:
                if response.status != 200:
                    app.logger.error(f"Request failed status code: {response.status}")
                    return response.status
                return await response.text()
    except Exception as e:
        app.logger.error(f"Exception in send_request: {e}")
        return None

async def send_multiple_requests(uid, server_name, url):
    try:
        region = server_name
        protobuf_message = create_protobuf_message(uid, region)
        if protobuf_message is None:
            app.logger.error("Failed create protobuf message.")
            return None
        encrypted_uid = encrypt_message(protobuf_message)
        if encrypted_uid is None:
            app.logger.error("Encryption failed.")
            return None
        tasks = []
        tokens = load_tokens(server_name)
        if tokens is None:
            app.logger.error("Failed to load tokens.")
            return None
        for i in range(100):
            token = tokens[i % len(tokens)]["token"]
            tasks.append(send_request(encrypted_uid, token, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    except Exception as e:
        app.logger.error(f"Exception in send_multiple_requests: {e}")
        return None

def create_uid_protobuf(uid):
    try:
        message = uid_generator_pb2.uid_generator()
        message.saturn_ = int(uid)
        message.garena = 1
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error creating uid protobuf: {e}")
        return None

def enc(uid):
    protobuf_data = create_uid_protobuf(uid)
    if protobuf_data is None:
        return None
    encrypted_uid = encrypt_message(protobuf_data)
    return encrypted_uid

def make_request(encrypt, server_name, token):
    try:
        if server_name == "IND":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
        elif server_name in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
        else:
            url = "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow"
        edata = bytes.fromhex(encrypt)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB53"
        }
        response = requests.post(url, data=edata, headers=headers, verify=False)
        hex_data = response.content.hex()
        binary = bytes.fromhex(hex_data)
        decode = decode_protobuf(binary)
        if decode is None:
            app.logger.error("Protobuf decoding returned None.")
        return decode
    except Exception as e:
        app.logger.error(f"Error in make_request: {e}")
        return None

def decode_protobuf(binary):
    try:
        items = like_count_pb2.Info()
        items.ParseFromString(binary)
        return items
    except DecodeError as e:
        app.logger.error(f"Error decoding Protobuf data: {e}")
        return None
    except Exception as e:
        app.logger.error(f"Unexpected error during protobuf decoding: {e}")
        return None

def fetch_player_info(uid):
    try:
        url = f"https://nr-codex-info.vercel.app/get?uid={uid}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            account_info = data.get("AccountInfo", {})
            return {
                "Level": account_info.get("AccountLevel", "NA"),
                "Region": account_info.get("AccountRegion", "NA"),
                "ReleaseVersion": account_info.get("ReleaseVersion", "NA")
            }
        else:
            app.logger.error(f"Player info API failed code: {response.status_code}")
            return {"Level": "NA", "Region": "NA", "ReleaseVersion": "NA"}
    except Exception as e:
        app.logger.error(f"Error fetching player info from API: {e}")
        return {"Level": "NA", "Region": "NA", "ReleaseVersion": "NA"}


# --- ROUTES ---

@app.route('/')
def serve_api_docs():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Core Service Console</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; background: #f9f9f9; }
            h1 { color: #111; border-bottom: 2px solid #eaeaea; padding-bottom: 10px; }
            h2 { color: #222; margin-top: 30px; }
            code { background: #272822; color: #f8f8f2; padding: 2px 6px; border-radius: 4px; font-family: "Courier New", Courier, monospace; font-size: 0.9em; }
            pre { background: #272822; padding: 15px; border-radius: 6px; overflow-x: auto; }
            pre code { background: none; color: #f8f8f2; padding: 0; }
            .endpoint-block { background: white; border: 1px solid #e1e4e6; border-left: 5px solid #0076ff; padding: 15px; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
            .endpoint-gift { border-left-color: #00bc7d; }
            .endpoint-like { border-left-color: #ff6b6b; }
            .badge { display: inline-block; padding: 3px 8px; font-size: 0.75em; font-weight: bold; border-radius: 3px; text-transform: uppercase; margin-right: 5px; color: white; }
            .badge-get { background: #0076ff; }
            .badge-web { background: #00bc7d; }
            .badge-like { background: #ff6b6b; }
        </style>
    </head>
    <body>
        <h1>API Microservices Portal</h1>
        <p>Welcome to the unified core system. Below are the available service endpoints configurations:</p>
        
        <div class="endpoint-block">
            <h3><span class="badge badge-get">GET</span> /token</h3>
            <p>Generates a dynamic JWT verification session signature via Garena Authenticator.</p>
            <p><strong>Example Syntax:</strong></p>
            <pre><code>node.venomexe.online:25570/token?access_token=YOUR_GARENA_ACCESS_TOKEN</code></pre>
        </div>

        <div class="endpoint-block endpoint-gift">
            <h3><span class="badge badge-web">WEB</span> /Gift</h3>
            <p>Launches the integrated graphical interface core mainframe dashboard platform.</p>
            <p><strong>Example Access:</strong></p>
            <pre><code>node.venomexe.online:25570/Gift</code></pre>
        </div>

        <div class="endpoint-block endpoint-like">
            <h3><span class="badge badge-like">GET</span> /like</h3>
            <p>Profile Like Booster - Sends 100 likes to target UID.</p>
            <p><strong>Example Syntax:</strong></p>
            <pre><code>node.venomexe.online:25570/like?uid=123456789&server_name=BD</code></pre>
        </div>
    </body>
    </html>
    """
    return html_content

@app.route('/Gift', methods=['GET'])
def serve_mainframe():
    # URL এ jwt প্যারামিটার আছে কিনা চেক করা হচ্ছে
    jwt_token = request.args.get('jwt')
    
    if jwt_token:
        # যদি jwt থাকে তাহলে API মেকানিজম রান করবে
        region, login_token = extract_jwt_payload(jwt_token)
        if not region:
            return jsonify({"success": False, "message": "CRITICAL: DECRYPTION REJECTED (INVALID JWT)"}), 400
            
        wallet_stats = dispatch_wallet_query(jwt_token, login_token, region)
        
        if wallet_stats.get("last_topup") == "SYNC_FAILED":
            return jsonify({
                "success": False,
                "message": "Failed to fetch wallet information from Garena Servers."
            }), 400
            
        return jsonify({
            "data": {
                "diamond": wallet_stats.get("diamond", 0),
                "gold": wallet_stats.get("gold", 0),
                "last_topup": wallet_stats.get("last_topup", "Never")
            },
            "region": region,
            "success": True
        })
    else:
        # যদি jwt না থাকে তাহলে নরমাল নিয়মে index.html টেমপ্লেট লোড হবে
        return render_template('index.html')

@app.route('/token', methods=['GET'])
def token_endpoint():
    access_token = request.args.get('access_token')
    if not access_token:
        return jsonify({"error": "Missing 'access_token' parameter"}), 400

    inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
    try:
        insp_resp = requests.get(inspect_url, timeout=10)
        if insp_resp.status_code != 200:
            return jsonify({"error": "Failed to inspect token", "status_code": insp_resp.status_code}), 400
        insp_data = insp_resp.json()
        open_id = insp_data.get('open_id')
        if not open_id:
            return jsonify({"error": "open_id not found in inspect response"}), 400
    except Exception as e:
        return jsonify({"error": f"Inspect request failed: {str(e)}"}), 500

    platform_types = [2, 3, 4, 6, 8]
    last_error = None
    for pt in platform_types:
        result = try_major_login(open_id, access_token, pt)
        if result:
            jwt_decoded = decode_jwt_full(result['token'])
            return jsonify({
                "success": True,
                "platform_type_used": pt,
                "jwt": result['token'],
                "jwt_decoded": jwt_decoded,
                "account_uid": result['account_uid'],
                "region": result['region'],
                "url": result['url'],
                "timestamp": result['timestamp']
            })
        else:
            last_error = f"Failed with platform_type {pt}"
            
    return jsonify({
        "success": False,
        "error": "MajorLogin failed. Account may be banned, not registered, or token invalid.",
        "detail": last_error
    }), 401

@app.route('/api/image/<item_id>')
def proxy_asset_image(item_id):
    try:
        img_res = requests.get(f"{IMAGE_BASE_URL}{item_id}.png", timeout=5)
        return Response(img_res.content, mimetype='image/png')
    except Exception: return "Asset Not Resolved", 404

@app.route('/api/get_store', methods=['POST'])
def fetch_matrix_store():
    payload = request.json
    jwt_token = payload.get('jwt')
    page = int(payload.get('page', 1))
    limit = int(payload.get('limit', 24))
    selected_category = payload.get('category', 'All')
    
    region, login_token = extract_jwt_payload(jwt_token)
    if not region: return jsonify({"success": False, "message": "CRITICAL: DECRYPTION REJECTED (INVALID JWT)"}), 400

    if jwt_token not in ZIBON_SYSTEM_CACHE:
        wallet_stats = dispatch_wallet_query(jwt_token, login_token, region)
        req_pb = GetGiftStoreDetails_pb2.CSGetGiftStoreDetailsReq(store_id=1)
        api_headers = {
            "Authorization": f"Bearer {jwt_token}", "X-GA": "v1 1", "ReleaseVersion": "OB53", 
            "Content-Type": "application/octet-stream", "User-Agent": CLIENT_AGENT_SPOOF
        }
        
        try:
            endpoint = f"{fetch_regional_endpoint(region)}/GetGiftStoreDetails"
            encrypted_payload = perform_aes_injection(req_pb.SerializeToString())
            res = requests.post(endpoint, data=encrypted_payload, headers=api_headers, verify=False, timeout=15)
            
            if res.status_code == 200:
                res_pb = GetGiftStoreDetails_pb2.CSGetGiftStoreDetailsRes()
                res_pb.ParseFromString(res.content)
                dict_converted = MessageToDict(res_pb, preserving_proto_field_name=True, always_print_fields_with_no_presence=True)
                
                compiled_items, unique_categories = [], set()
                for proto_item in dict_converted.get('items', []):
                    str_id = str(proto_item.get('item_id', '0'))
                    cat_title = CATEGORY_MAP_PRO.get(str_id[:3], f"Unassigned ({str_id[:3]})")
                    unique_categories.add(cat_title)
                    
                    diamonds = int(proto_item.get('gems_price', 0))
                    coins = int(proto_item.get('coins_price', 0))
                    
                    price_lbl = "Free Tier"
                    if diamonds > 0 and coins > 0: price_lbl = f"💎 {diamonds} / 🪙 {coins}"
                    elif diamonds > 0: price_lbl = f"💎 {diamonds}"
                    elif coins > 0: price_lbl = f"🪙 {coins}"
                    
                    expiry_timestamp = int(proto_item.get('expire_timestamp', 0))
                    date_lbl = datetime.fromtimestamp(expiry_timestamp).strftime('%d %b %Y') if expiry_timestamp > 0 else "Lifetime Asset"

                    compiled_items.append({
                        "item_id": str_id, "commodity_id": proto_item.get('commodity_id'),
                        "sort_id": int(proto_item.get('sort_id', 0)), "price_str": price_lbl,
                        "category": cat_title, "expire_date": date_lbl
                    })

                compiled_items.sort(key=lambda x: x['sort_id'], reverse=True)
                ZIBON_SYSTEM_CACHE[jwt_token] = {
                    'items': compiled_items, 'wallet': wallet_stats, 
                    'sent': dict_converted.get('send_gift_times_today', 0), 'cats': sorted(list(unique_categories))
                }
            else: return jsonify({"success": False, "message": "Garena Core Server Refused Response Code"}), 400
        except Exception as err: return jsonify({"success": False, "message": f"Fatal Core Exception: {str(err)}"}), 500

    cached_data = ZIBON_SYSTEM_CACHE[jwt_token]
    filtered_output = [x for x in cached_data['items'] if x['category'] == selected_category] if selected_category != "All" else cached_data['items']
    offset = (page - 1) * limit
    
    return jsonify({
        "success": True, "items": filtered_output[offset : offset + limit], 
        "categories": cached_data['cats'], "wallet": cached_data['wallet'], 
        "sent_today": cached_data['sent'], "has_more": (offset + limit) < len(filtered_output)
    })

@app.route('/api/send_gift', methods=['POST'])
def pipe_gift_transmission():
    req_payload = request.json
    jwt = req_payload.get('jwt')
    target_uid = req_payload.get('receiver_uid')
    comm_id = req_payload.get('commodity_id')
    unit_price = req_payload.get('price')
    currency_type = req_payload.get('currency')
    custom_message = req_payload.get('message', 'Gift Dispatch!')
    
    region, _ = extract_jwt_payload(jwt)
    if not region: return jsonify({"success": False, "message": "EXPLOIT DENIED: TOKEN AUTH DISCREPANCY"}), 400

    pb_request = SendGift_pb2.CSSendGiftReq()
    pb_request.receiver_account_ids.append(int(target_uid))
    pb_request.buddy_type = 1
    pb_request.commodity_id = int(comm_id)
    pb_request.message_content = custom_message
    pb_request.currency_type = 2 if currency_type == 'diamond' else 1
    pb_request.commodity_cnt = 1
    pb_request.unit_price = int(unit_price)

    api_headers = {
        "Authorization": f"Bearer {jwt}", "X-GA": "v1 1", "ReleaseVersion": "OB53", 
        "Content-Type": "application/octet-stream", "User-Agent": CLIENT_AGENT_SPOOF
    }
    
    try:
        endpoint_url = f"{fetch_regional_endpoint(region)}/SendGift"
        encrypted_body = perform_aes_injection(pb_request.SerializeToString())
        res = requests.post(endpoint_url, data=encrypted_body, headers=api_headers, verify=False, timeout=15)
        
        if res.status_code == 200:
            if jwt in ZIBON_SYSTEM_CACHE: del ZIBON_SYSTEM_CACHE[jwt]
            return jsonify({"success": True, "message": f"✓ SUCCESS: Packet injected. Gift transmitted to UID: {target_uid}"})
        else:
            try: return_error = res.content.decode('utf-8').strip()
            except Exception: return_error = f"HTTP STATUS CODE: {res.status_code}"
            return jsonify({"success": False, "message": f"✖ TRANSMIT REFUSED: {return_error}"})
    except Exception as e: 
        return jsonify({"success": False, "message": f"💥 CRITICAL PIPELINE CORRUPTION: {str(e)}"})

@app.route('/like', methods=['GET'])
def handle_like_requests():
    uid = request.args.get("uid")
    server_name = request.args.get("server_name", "").upper()
    if not uid or not server_name:
        return jsonify({"error": "UID and server_name are required"}), 400

    try:
        def process_request():
            player_info = fetch_player_info(uid)
            region = player_info["Region"]
            level = player_info["Level"]
            release_version = player_info["ReleaseVersion"]

            if region != "NA" and server_name != region:
                app.logger.warning(f"Server name {server_name} does not match API region {region}. Using API region.")
                server_name_used = region
            else:
                server_name_used = server_name

            tokens = load_tokens(server_name_used)
            if tokens is None:
                raise Exception("Failed to load tokens.")
            token = tokens[0]['token']
            encrypted_uid = enc(uid)
            if encrypted_uid is None:
                raise Exception("Encryption of UID failed.")

            before = make_request(encrypted_uid, server_name_used, token)
            if before is None:
                raise Exception("Failed to retrieve initial player info.")
            try:
                jsone = MessageToJson(before)
            except Exception as e:
                raise Exception(f"Error converting 'before' protobuf to JSON: {e}")
            data_before = json.loads(jsone)
            before_like = data_before.get('AccountInfo', {}).get('Likes', 0)
            try:
                before_like = int(before_like)
            except Exception:
                before_like = 0
            app.logger.info(f"Likes before command: {before_like}")

            if server_name_used == "IND":
                url = "https://client.ind.freefiremobile.com/LikeProfile"
            elif server_name_used in {"BR", "US", "SAC", "NA"}:
                url = "https://client.us.freefiremobile.com/LikeProfile"
            else:
                url = "https://clientbp.ggpolarbear.com/LikeProfile"

            asyncio.run(send_multiple_requests(uid, server_name_used, url))

            after = make_request(encrypted_uid, server_name_used, token)
            if after is None:
                raise Exception("Failed to retrieve player info after like requests.")
            try:
                jsone_after = MessageToJson(after)
            except Exception as e:
                raise Exception(f"Error converting 'after' protobuf to JSON: {e}")
            data_after = json.loads(jsone_after)
            after_like = int(data_after.get('AccountInfo', {}).get('Likes', 0))
            player_uid = int(data_after.get('AccountInfo', {}).get('UID', 0))
            player_name = str(data_after.get('AccountInfo', {}).get('PlayerNickname', ''))
            like_given = after_like - before_like
            status = 1 if like_given != 0 else 2
            result = {
                "LikesGivenByAPI": like_given,
                "LikesafterCommand": after_like,
                "LikesbeforeCommand": before_like,
                "PlayerNickname": player_name,
                "Region": region,
                "Level": level,
                "UID": player_uid,
                "ReleaseVersion": release_version,
                "status": status
            }
            return result

        result = process_request()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 25570))
    app.run(host='0.0.0.0', port=PORT, debug=False)
