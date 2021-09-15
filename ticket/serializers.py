from rest_framework import serializers

class InsuredSerializer(serializers.ModelSerializer):

    def get_user_name(self, obj):
        return obj.user.username

    def get_first_name(self, obj):
        return obj.user.first_name

    username = serializers.SerializerMethodField("get_user_name")
    first_name = serializers.SerializerMethodField("get_first_name")

    class Meta:
        model = Insured

        fields = ['id', 'user','username', 'first_name','insurance', 'is_holder',
                  'supported_insureds', 'bank_account_number']
