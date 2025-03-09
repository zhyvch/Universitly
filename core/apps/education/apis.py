from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.apps.education.models import Institution, Course, Section
from core.apps.education.services import DjangoORMInstitutionService, DjangoORMCourseService


class InstitutionCreateAPI(APIView):
    service = DjangoORMInstitutionService()

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Institution
            fields = ['title', 'type', 'icon']

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.create_institution(
            user=request.user,
            **serializer.validated_data,
        )

        return Response(status=status.HTTP_201_CREATED)


class InstitutionListAPI(APIView):
    service = DjangoORMInstitutionService()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Institution
            fields = '__all__'

    def get(self, request):
        institution_list = self.service.selector.get_institution_list()
        data = self.OutputSerializer(institution_list, many=True).data

        return Response(data=data)


class InstitutionUpdateAPI(APIView):
    service = DjangoORMInstitutionService()

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Institution
            fields = ['title', 'type', 'icon']


    def patch(self, request, institution_id):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.service.update_institution(
            user=request.user,
            institution_id=institution_id,
            **serializer.validated_data,
        )

        return Response(status=status.HTTP_200_OK)


class InstitutionDeleteAPI(APIView):
    service = DjangoORMInstitutionService()

    def delete(self, request, institution_id):
        self.service.delete_institution(
            user=request.user,
            institution_id=institution_id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseCreateAPI(APIView):
    service = DjangoORMCourseService()

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ['title', 'teachers', 'students']

    def post(self, request, institution_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.create_course(
            user=request.user,
            institution_id=institution_id,
            **serializer.validated_data,
        )

        return Response(status=status.HTTP_201_CREATED)


class CourseListAPI(APIView):
    service = DjangoORMCourseService()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = '__all__'

    def get(self, request, institution_id):
        course_list = self.service.selector.get_course_list(
            user_id=request.user.id,
            institution_id=institution_id
        )
        data = self.OutputSerializer(course_list, many=True).data

        return Response(data=data)
