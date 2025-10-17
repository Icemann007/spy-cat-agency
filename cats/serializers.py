import decimal

import requests
from django.conf import settings
from rest_framework import serializers

from cats.models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["id", "name", "years_of_experience", "breed", "salary"]
        read_only_fields = ["id"]

    def validate_breed(self, value):
        try:
            response = requests.get(settings.CAT_API_URL, timeout=10)
            response.raise_for_status()
            breeds = response.json()

            valid_breeds = [breed["name"].lower() for breed in breeds]

            if value.lower() not in valid_breeds:
                raise serializers.ValidationError(
                    f"Invalid breed '{value}'. Must be a valid cat breed."
                )

            return value
        except requests.RequestException as e:
            raise serializers.ValidationError(f"Unable to validate breed: {str(e)}")

    def validate_salary(self, value):
        if value <= decimal.Decimal("0.00"):
            raise serializers.ValidationError("Salary must be a positive value.")

        return value


class CatSalaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["salary"]
