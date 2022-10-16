# from datetime import date
from rest_framework import serializers
from users.models import User
import string


class UserSerializer(serializers.ModelSerializer):

	repeat_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['username', 'age', 'email', 'password', 'repeat_password']
		# fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	

	def validate_password(self, value):
		whitespace_value = ' ' in value
		value_length = len(value)
		upper_value = False
		lower_value = False
		uppercase="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		lowercase="abcdefghijklmnopqrstuvwxyz"
		for ele in value:
			if(ele in uppercase):
				upper_value=True
				break
		for ele1 in value:
			if(ele1 in lowercase):
				lower_value=True
				break
		
		NON_ALPHABETIC_CHARACTERS = {
		'#',
		'!',
		'$',
		'@',
		'%'
		}
		DIGITS_CHARACTERS = set(string.digits)
		LETTERS_CHARACTERS = set(string.ascii_letters)

		ALLOWED_CHARACTERS = (NON_ALPHABETIC_CHARACTERS | DIGITS_CHARACTERS | LETTERS_CHARACTERS)

		non_alphabetic_characters = NON_ALPHABETIC_CHARACTERS
		digits_characters = DIGITS_CHARACTERS
		letters_characters = LETTERS_CHARACTERS
		allowed_characters = ALLOWED_CHARACTERS


		if not any(character in value for character in non_alphabetic_characters):
			raise serializers.ValidationError({'password': 'Passwords must contain atleast one special character.'})
		elif not any(character in value for character in digits_characters):
			raise serializers.ValidationError({'password': 'Password should contain at least one digit character.'})
		elif not any(character in value for character in letters_characters):
			raise serializers.ValidationError({'password': 'Password should contain at least one letter character.'})
		elif not all(character in allowed_characters for character in value):
			raise serializers.ValidationError({'password': 'Invalid Password!'})	
		elif  whitespace_value == True:
			raise serializers.ValidationError({'password': 'Passwords contains white space.'})
		elif value_length < 7: 
			raise serializers.ValidationError({'password': 'Passwords should be atleast 7 letters'})
		elif upper_value == False:
			raise serializers.ValidationError({'password': 'Passwords should be contains atleast 1 Upper Case'})
		elif lower_value == False:
		 	raise serializers.ValidationError({'password': 'Passwords should be contains atleast 1 Lower Case'})
		return value


	def	save(self):

		user = User(
					email=self.validated_data['email'],
					username=self.validated_data['username'],
					age=self.validated_data['age'],
				)

	
		password = self.validated_data['password']
	

		repeat_password = self.validated_data['repeat_password']
		if password != repeat_password:
			raise serializers.ValidationError({'password': 'Passwords must match.'})

		user.set_password(password)
        


		user.save()
		return user


# class UserSerializer(serializers.ModelSerializer):
#     # username = serializers.CharField(max_length=7)
#     # age = serializers.DateField()
#     # email = serializers.EmailField(max_length=254)
#     # password = serializers.CharField(max_length=254)
#     # repeat_password = serializers.CharField(max_length=254)
#     class Meta:
#         model = User
#         fields = '__all__'
#         # fields = ['username', 'age', 'email', 'password', 'repeat_password']

#         def perform_create(self, serializer):
#             queryset = User.objects.filter(email=self.request.user)
#             if queryset.exists():
#                 raise serializers.ValidationError('You have already signed up')
#             serializer.save(user=self.request.user)
