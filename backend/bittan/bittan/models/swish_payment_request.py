from django.db import models
from djmoney.models.fields import MoneyField
from django_enumfield import enum

class PaymentStatus(enum.Enum):
	PAID = 1,
	CANCELLED = 2,
	WAITING = 3,

	# __SWISH_API_STATUS_MAPPINGS = {
	# 	# TODO Fill in the types when swish docs are updated
	# 	"CANCELLED": CANCELLED,
	# 	"WAITING": WAITING, # I have no idea if this is a response we can have 
	# 	"PAID": PAID,
	# }

	@staticmethod
	def from_swish_api_status(status: str):
		# TODO Fix when docs are updated
		print("GOT status: " + status)
		return PaymentStatus[status]

class PaymentErrorCode(enum.Enum):
	UNKNOWN = 0
	FAILED_TO_INITIATE = 1
	# TIMEOUT = 1
	# CANCELLED_BY_USER = 2
	# CANCELLED_OTHER = 3
	
	# __SWISH_ERROR_CODE_MAPPINGS = {
	# 	"RF07": CANCELLED_OTHER,
	# 	"BANKIDCL": CANCELLED_BY_USER,
	# 	"FF10": ERROR,
	# 	"TM01": TIMEOUT,

	# 	"DS24": ERROR,  # SE TILL ATT DETTA HANTERAS SPECIELLT

	# 	"VR01": ERROR,
	# 	"VR02": ERROR,
	# }

	@staticmethod
	def from_swish_reponse_code(status: str|None):
		if status == None:
			return None

		return PaymentErrorCode.UNKNOWN
		# return PaymentErrorCode.__SWISH_ERROR_CODE_MAPPINGS[status]


class SwishPaymentRequestModel(models.Model):
	# time_created = models.DateTimeField(auto_now_add=True)
	id = models.TextField(primary_key=True)
	status = enum.EnumField(PaymentStatus, default=PaymentStatus.WAITING)
	error_code = enum.EnumField(PaymentErrorCode, null=True)

	amount = models.IntegerField()

	external_uri= models.TextField(null=True)

	token = models.TextField(null=True)

	swish_api_response = models.TextField(null=True)
	
	def fail(self, fail_reason: PaymentErrorCode):
			self.status = PaymentStatus.CANCELLED
			self.error_code = fail_reason