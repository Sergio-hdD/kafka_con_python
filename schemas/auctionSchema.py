from importsAndConfigsApp import ma 


class AuctionSchema(ma.Schema):
	class Meta:
		fields = (
				'id',
				'id_user_creator',
				'id_product',
				'amount_base',
				'start_date',
				'end_date',
				'id_user_last_offer', 
				'date_last_offer',
				'last_amount_offered'
				)