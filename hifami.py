import requests
import aiohttp
import asyncio

# إعدادات الهيدرز الأساسية
headers = {
    'Host': 'api.wepartytt.com',
    'apikey': '3d124ec3',
    'codetag': 'weparty-6.3.100',
    'channel': 'market_guanwang',
    'memberid': '60b5adca3df478f7d7c12503bc03707e',
    'authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaGFubmVsX25hbWUiOiJtYXJrZXRfZ3VhbndhbmciLCJjb2RlX3RhZyI6IndlcGFydHktNi4zLjEwMCIsImV4cGlyZV9hdCI6IjIwMjQtMTItMzAgMDE6NTI6MjMiLCJpZCI6MTA2ODA4MzcsInN0YXR1cyI6MH0._FZdLtOC-1q-OYL_E4DUrSQfE7RfVukuWhD5HrCjABc',
    'osversion': '11',
    'brand': 'nokia',
    'user-agent': 'weparty-Android-Mozilla/5.0 (Linux; Android 11; Infinix X695 Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36',
    'versionname': '6.3.100',
    'timestamp': '1735474251',
    'requesttimestampinms': '1735474251508',
    'noncestr': '4312d2971566495aa19365526c7989f1',
    'environment': 'unknown',
    'rcsign': 'cec29caa179e6961e75776d9fba936a7d870997ebc8caf0f49fbdda5149e4777431e39c7ac40d8e07049a59eb85b6e38d34e02eb404faf870b83e588500e43c75de7e91a1b4536fb296c499d2ab35edac854c2e3bdb759712316b4122bc41bb9c1512fc85d7eb0e69002011dc4140ee917d912c40fc19357f30bca4201c42833eff7537f020621b8f1482cf0db8fa900cec98c2a24ac1fe76f47ea4a72c427d4f382729ad93be9543d260bef8cbe480c4715da8c219e4b08f75f29aa08201b504f8090838588fd5877cee1fa7811ce8d61b715d6799126d81acd12470b141b2ae231a88873bccb766a0ad3f9db622c64',
    'isforeground': 'true',
    'refer_page': 'main_page',
    'language': 'ar',
    'timezone': 'Africa/Cairo',
    'ispublish': 'true',
    'isocode': 'EG',
    'risktoken': 'F8D67CAE451EECDB5DBA2860EB249CAF',
    'signtoken': 'BC5AD2340AB2D1996180321CAFD42249',
    'umid': '158018e5dc70ab76ac1c22b1c35f98fd',
    'content-length': '0',
    'accept-encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# دالة لتحديث الـ Authorization باستخدام الـ API
def refresh_auth():
    url = "https://api.wepartytt.com/auth/v6/login"
    data = {
        "code": "363f97c47a0e322aae117c26ffd392ac5b13f79fe7d13ef1f8bd71f943b1bf76",
        "id": "b5b0595289c59afc8189abc89270546c"
    }
    try:
        # إرسال البيانات باستخدام data بدلاً من json
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            auth_token = response.json().get("data", {}).get("token")
            if auth_token:
                headers["authorization"] = auth_token
                print("تم تحديث التوكن بنجاح!")
            else:
                print("فشل في تحديث التوكن!")
        else:
            print(f"خطأ في تحديث التوكن: {response.status_code}, التفاصيل: {response.text}")
    except Exception as e:
        print(f"خطأ أثناء التحديث: {e}")
# دالة لجلب بيانات التعدين
def get_mining_info():
    url = "https://api.wepartytt.com/member-asset/v6/game/mining/info"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("تم التحقق من أن التوكن انتهت صلاحيته. تحديث التوكن الآن...")
            refresh_auth()  # تحديث التوكن عند انتهاء صلاحيته
            return get_mining_info()  # إعادة المحاولة بعد التحديث
        else:
            print(f"خطأ في جلب البيانات: {response.status_code}, التفاصيل: {response.text}")
            return None
    except Exception as e:
        print(f"خطأ أثناء الإرسال: {e}")
        return None

# دالة لتطوير المستوى
def upgrade_level():
    url = "https://api.wepartytt.com/member-asset/v6/game/mining/up_level"
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"تم تطوير المستوى! النقاط المخصومة: {data['data']['mineral_num']}")
        else:
            print(f"خطأ في التطوير: {response.status_code}, التفاصيل: {response.text}")
    except Exception as e:
        print(f"خطأ أثناء الإرسال: {e}")

# دالة لإرسال 100 طلب حصاد بالتوازي
async def send_harvest_requests():
    url = 'https://api.wepartytt.com/member-asset/v6/game/mining/harvest'

    async def send_request(session):
        try:
            async with session.post(url, headers=headers) as response:
                await response.json()  # معالجة الرد
        except asyncio.TimeoutError:
            pass
        except Exception as e:
            pass

    num_requests = 100  # عدد الطلبات
    max_connections = 100  # الحد الأقصى للاتصالات المفتوحة
    timeout = aiohttp.ClientTimeout(total=10)  # إجمالي مهلة الطلب (بالثواني)

    connector = aiohttp.TCPConnector(limit=max_connections)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [send_request(session) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

# دالة لجلب بيانات الحزمة الحمراء
def get_red_packet_info():
    url = "https://api.wepartytt.com/cash_requests/v6/red_packets_info?country=EG"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"خطأ في جلب بيانات الحزمة الحمراء: {response.status_code}, التفاصيل: {response.text}")
            return None
    except Exception as e:
        print(f"خطأ أثناء الإرسال: {e}")
        return None

# الدالة الرئيسية
def main():
    while True:
        # الحصول على بيانات التعدين
        data = get_mining_info()
        if data and data.get("code") == 0:
            mining_asset = data["data"]["mining_asset"]
            mining_data = data["data"]["mining_data"]
            
            mineral_num = mining_asset["mineral_num"]
            upgrade_need_mineral_num = mining_data["upgrade_need_mineral_num"]
            remain_seconds = mining_data.get("remain_seconds")  # ممكن تختفي

            print(f"المعادن الحالية: {mineral_num}, المستوى الحالي: {mining_data['curr_level']}")

            # التحقق من إمكانية تطوير المستوى
            if mineral_num >= upgrade_need_mineral_num:
                upgrade_level()
            else:
                print("لا يمكن تطوير المستوى الآن. سيتم تنفيذ الحصاد.")
                if remain_seconds is not None:
                    print(f"انتظار {remain_seconds + 2} ثانية...")
                    asyncio.run(asyncio.sleep(remain_seconds + 2))
                
                # إرسال طلب الحصاد
                asyncio.run(send_harvest_requests())
                
                # تحديث بيانات التعدين بعد الحصاد
                updated_data = get_mining_info()
                if updated_data and updated_data.get("code") == 0:
                    updated_mineral_num = updated_data["data"]["mining_asset"]["mineral_num"]
                    added_minerals = updated_mineral_num - mineral_num
                    load_cap_max = updated_data["data"]["mining_data"]["load_cap_max"]
                    num_of_added = added_minerals / load_cap_max
                    print(f"تم تنفيذ الحصاد {num_of_added:.2f} مرة.")
                    print(f"تم إضافة {added_minerals} نقطة بعد الحصاد.")

                # جلب بيانات الحزمة الحمراء
                red_packet_data = get_red_packet_info()
                if red_packet_data and red_packet_data.get("code") == 0:
                    currency = red_packet_data["data"]["currency"] / 100  # تحويل إلى الجنيه
                    total_money = red_packet_data["data"]["total_money"] / 100  # تحويل إلى الدولار
                    print(f"الرصيد بالجنيه: {currency:.2f} جنيه.")
                    print(f"الرصيد بالدولار: {total_money:.2f} دولار.")
        else:
            print("فشل في جلب بيانات التعدين!")
            break

if __name__ == "__main__":
    main()