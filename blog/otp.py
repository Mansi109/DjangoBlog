import requests
import random

def SendOtp(mobile):
	otp=random.randint(1000,9999)
	dict = {
	"mobile":'+91'+str(mobile),
	"otp":otp,
	"message":'your otp is '+str(otp),
	"authkey":"280095AOG9gcp1RBrL5cfb4330",
	"sender":"VADESK"
	}
	print(dict)
	requests.post('https://control.msg91.com/api/sendotp.php?', data=dict)

	return otp



def VerifyOtp(mobile, otp):
	dict = {
	"mobile":'+91'+str(mobile),
	"otp":otp,
	"authkey":"280095AOG9gcp1RBrL5cfb4330"
	}
	r = requests.post('https://control.msg91.com/api/verifyRequestOTP.php',data = dict)
	if r.status_code==200:
		data = r.json()
		print(data)
		if data.get('type') == 'success':
			return 1
		else:
			return 0
	else:
		return -1





print(SendOtp(7210977769))
#print(VerifyOtp(8840565787,1234))