import hashlib
import vonage
import random

# password hashing
def sha256(data):
    data=bytes(data,'utf-8')
    sha=hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

def uniqueId(id):
    uid=''.join([str(random.randint(0, 9)) for _ in range(10)])
    if uid in id:
        return uniqueId(id)
    else:
        return uid

#creating client service
client = vonage.Client(key="600eb289", secret="GUdtunPwXOEde1Uu")
sms = vonage.Sms(client)

#otp sending 
def sendOTP(phone):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    responseData = sms.send_message(
        {
            "from": "LMS",
            "to": phone,
            "text": "Your OTP for LMS registration is {0}.Do not share!".format(otp),
        }
    )
    if responseData["messages"][0]["status"] == "0":
        return otp


