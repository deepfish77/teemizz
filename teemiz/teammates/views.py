from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, View, ListView
from .models import Team
from teammates.forms import TeamCreateForm
from teammates.models import TeamPositions
from projects.models import Project
from teammates.serializers import TeamSerializer, TeamCreateSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from .forms import RegisterForm

User = get_user_model()

# Team Views


class TeamFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Team.objects.toggle_follow(
            request.user, username_to_toggle)
        return redirect(f"/u/{profile_.user.username}/")


class TeamDetailView(ListView):
    template_name = 'team_list.html'

    def get_queryset(self):
        print("kwargs" + str(self.kwargs.get))

        slug = self.kwargs.get("slug")
        print("THe slug :", slug)
        if slug:
            queryset = Team.objects.filter(name=slug)
            print("QUER: " + str(queryset))
        else:
            queryset = Team.objects.all()
            print("QUERAllpy: " + str(queryset.all()))
        return queryset  # ListView.get_queryset(self)


class TeamListView(DetailView):
    template_name = 'team_list.html'

    queryset = Team.objects.all()
    print("team detail query set", queryset)

    for query in queryset:
        print(query.slug)

    def get_context_data(self, **kwargs):
        print("The args are:" + str(kwargs))
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")

        if slug:
            queryset = Team.objects.filter(name=slug)
            print("QUER: " + str(queryset))
        else:
            queryset = Team.objects.all()
            print("QUERAllpy: " + str(queryset.all()))
        return queryset  # ListView.get_queryset(self)

        pk = self.kwargs.get('slug')
        print("team_id_is_d", pk)

        obj = get_object_or_404(Team, id=slug)
        return obj


class TeamCreateView(CreateView):
    template_name = 'form.html'
    form_class = TeamCreateForm


# Team Position Views
class TeamPositionView(ListView):
    def get_queryset(self):
        print("TheTeam: ", self.request.team)
        return TeamPositions.objects.filter(team=self.requeset.team)


# Team API - need to implement with CSRF validation
@csrf_exempt
def team_api_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        print("the teams from api", teams)
        serializer = TeamSerializer(teams, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print("ThePostReq", request)
        data = JSONParser().parse(request)
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def team_api_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TeamSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        print("TheReq", request)
        data = JSONParser().parse(request)
        serializer = TeamSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


class TeamAPI(APIView):

    def get(self, request, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("requestdata:", request.data)
        serializer = TeamCreateSerializer(data=request.data)
        print("teamseri:", serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamApiDetail(APIView):
    """
    Retrieve, update or delete a team instance.
    """

    def get_object(self, pk):
        try:
            print("pk", pk)
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = Team(team)
        print("The Teams List", team)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        team = self.get_object(pk)
        serializer = Team(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team = self.get_object(pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomeView(View):

    def get(self, request, *args, **kwargs):
        # if  request.user.is_authenticated():
        teams_list = Team.objects.all()
        projects_list = Project.objects.all()
        team_positions = TeamPositions.objects.all()
        print("The Teams List", teams_list)
        print("The Projects List", projects_list)
        return render(request, "home.html", {"teams": teams_list, "projects": projects_list, "positions": team_positions})


class TeamFullView(View):

    def get(self, request, *args, **kwargs):

        slug = self.kwargs.get("slug")
        print("THe slug full View :", slug)
        if slug:
            current_team = Team.objects.filter(slug=slug)

            team_id = set(current_team.values_list('id',  flat=True))
            print('teamid', team_id)

            team_positions = TeamPositions.objects.filter(
                related_team_id=team_id.pop())
            print('the team positions ', team_positions.values())
            queryset = current_team.get()

            print("QUER: ", queryset)
        else:
            raise Http404()

        return render(request, "team_detail.html", {"team": queryset, "team_positions": team_positions})
