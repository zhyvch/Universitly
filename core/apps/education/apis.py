from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.education.models import Institution
from core.apps.education.selectors import DjangoORMInstitutionSelector
from core.apps.education.services import DjangoORMInstitutionService


class InstitutionCreateAPI(APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=True)
        type = serializers.ChoiceField(choices=Institution.InstitutionType, required=False)
        icon = serializers.ImageField(required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = DjangoORMInstitutionService()
        service.create_institution(
            owner=request.user,
            **serializer.validated_data,
        )

        return Response(status=status.HTTP_201_CREATED)


class InstitutionListAPI(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        type = serializers.ChoiceField(choices=Institution.InstitutionType)
        icon = serializers.ImageField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def get(self, request):
        selector = DjangoORMInstitutionSelector()
        institution_list = selector.get_institution_list()
        data = self.OutputSerializer(institution_list, many=True).data

        return Response(data=data)


class InstitutionUpdateAPI(APIView):
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        type = serializers.ChoiceField(choices=Institution.InstitutionType, required=False)
        icon = serializers.ImageField(required=False)

    def patch(self, request, institution_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = DjangoORMInstitutionService()
        service.update_institution(
            owner=request.user,
            institution_id=institution_id,
            **serializer.validated_data,
        )

        return Response(status=status.HTTP_200_OK)


class InstitutionDeleteAPI(APIView):
    def delete(self, request, institution_id):
        service = DjangoORMInstitutionService()
        service.delete_institution(
            owner=request.user,
            institution_id=institution_id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
