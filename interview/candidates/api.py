from rest_framework import serializers, generics
from django.db.models import Q
from .models import Candidate

   
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateListAPI(generics.ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        last_name = self.request.GET.get('last_name')
        first_name = self.request.GET.get('first_name')
        query = self.request.GET.get('query')

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        elif first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        elif query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return queryset