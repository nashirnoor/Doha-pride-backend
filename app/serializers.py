# serializers.py
from rest_framework import serializers
from .models import TransferMeetAssist, Point

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'text']

class TransferMeetAssistSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = TransferMeetAssist
        fields = ['id', 'name', 'description_one', 'points', 'description_two', 'cost', 'image']

    def create(self, validated_data):
        points_data = self.context['request'].data.get('points', [])
        transfer_meet_assist = TransferMeetAssist.objects.create(**validated_data)
        for point_data in points_data:
            Point.objects.create(transfer_meet_assist=transfer_meet_assist, text=point_data['text'])
        return transfer_meet_assist

    def update(self, instance, validated_data):
        points_data = self.context['request'].data.get('points', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description_one = validated_data.get('description_one', instance.description_one)
        instance.description_two = validated_data.get('description_two', instance.description_two)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        instance.points.all().delete()
        for point_data in points_data:
            Point.objects.create(transfer_meet_assist=instance, text=point_data['text'])
        return instance