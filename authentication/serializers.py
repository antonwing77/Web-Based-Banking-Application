from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    
    class Meta:
        model = User
        fields = ['id','username','email','password','role']
        read_only_fields = ['id','role']  # role only set by admins

    def create(self, validated_data):
        pw = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(pw)
        user.save()
        
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_old_password(self, old_pw):
        user = self.context['request'].user
        if not user.check_password(old_pw):
            raise serializers.ValidationError("Old password is incorrect")
        
        return old_pw

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

        return user