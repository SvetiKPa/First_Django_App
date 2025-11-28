from rest_framework import serializers
from tasks_app.models import Category
from django.core.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create_category(self, validated_data):
        name = validated_data.get('name')

        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({
                'name': 'Категория с таким названием уже существует.'
            })
        try:
            category = Category.objects.create(**validated_data)
            return category
        except Exception as e:
            raise serializers.ValidationError({
                'error': f'Ошибка при создании категории: {str(e)}'
            })

    def update_category(self, instance, validated_data):
        name = validated_data.get('name')
        if name and name != instance.name:
            # Проверяем, существует ли другая категория с таким названием
            if Category.objects.filter(name__iexact=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError({
                    'name': 'Категория с таким названием уже существует.'
                })

        try:
            # Обновляем категорию
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({
                'error': f'Ошибка при обновлении категории: {str(e)}'
            })


