from rest_framework import serializers

class LaptopSerializer(serializers.Serializer):
    Status = serializers.CharField()
    Brand = serializers.CharField()
    Model = serializers.CharField()
    CPU = serializers.CharField()
    RAM = serializers.FloatField()
    Storage = serializers.FloatField()
    Storage_type = serializers.CharField() # Use underscores or match your HTML name
    GPU = serializers.CharField()
    Screen = serializers.FloatField()
    Touch = serializers.CharField()