import io

from django.shortcuts import HttpResponse, render
from icalendar import Calendar, Event

from .models import Candidate, Interview


def candidates_list(request):
    last_name = request.GET.get('last_name')
    first_name = request.GET.get('first_name')

    if last_name:
        candidates = Candidate.objects.filter(last_name__icontains=last_name)
    elif first_name:
        candidates = Candidate.objects.filter(first_name__icontains=first_name)
    else:
        candidates = Candidate.objects.all()

    interviews = Interview.objects.all()
    unique_candidates = interviews.distinct('candidate')
    print(unique_candidates)
    context = {
        'interviews':unique_candidates,
        'candidates': candidates
    }
    return render(request, "candidates/list.html", context)

def candidate_ics_view(request, pk):
    candidate = Candidate.objects.get(pk=pk)
    interviews = candidate.interviews.all()
    calendar = Calendar()
    event = Event()
    for interview in interviews:
        event.add('Candidate Name', f"{interview.candidate.first_name} {interview.candidate.last_name}")
        event.add('Time', interview.time)
        event.add('status', interview.status)
        event.add('feedback', interview.feedback)
        calendar.add_component(event)

    ics_file = io.BytesIO()
    ics_file.write(calendar.to_ical())
    ics_file.seek(0)

    response = HttpResponse(ics_file, content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="candidate_interviews.ics"'
    return response