from django.contrib.auth.models import User
from django.db.models import Prefetch

from rest_framework import routers, viewsets
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from models import Article, Topic, HighlightGroup, Project, Question, Answer, ArticleHighlight, UserProfile
from serializers import (UserProfileSerializer, ArticleSerializer,
                         TopicSerializer, HighlightGroupSerializer,
                         ProjectSerializer, QuestionSerializer,
                         ArticleHighlightSerializer, RootTopicSerializer,
                         SubmittedAnswerSerializer)

# Views for serving the API

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.filter(parent=None)
    serializer_class = RootTopicSerializer

class HighlightGroupViewSet(viewsets.ModelViewSet):
    queryset = HighlightGroup.objects.all()
    serializer_class = HighlightGroupSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.DATA, list):
            serializer = HighlightGroupSerializer(data=request.DATA, many=True)
            if serializer.is_valid():
                self.object = serializer.save(force_insert=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return super(HighlightGroupViewSet, self).create(request, *args, **kwargs)

class ArticleHighlightViewSet(viewsets.ModelViewSet):
    queryset = ArticleHighlight.objects.all()
    serializer_class = ArticleHighlightSerializer

@api_view(['GET'])
def topic(request, id):
    """
    /topics/id \n
    Gets all the information associated with a specific topic.
    """
    if request.method == 'GET':
        topics = Topic.objects.get(id=id)
        serializer = TopicSerializer(topics, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def child_topics(request, id):
    """
    /topics/id/children \n
    Gets all the child topics of a topic.
    """
    if request.method == 'GET':
        topics = Topic.objects.get(parent=Topic.objects.get(id=id))
        serializer = TopicSerializer(topics, many=False)
        return Response(serializer.data)


@api_view(['GET'])
def questions(request):
    """
    /question
    Gets all the questions.
    """
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def question(request, id):
    """
    /question/id
    Gets a specific question.
    """
    if request.method == 'GET':
        question = Question.objects.get(id=id)
        serializer = QuestionSerializer(question, many=False)
        return Response(serializer.data)

@api_view(['GET'])
def next_question(request, id, ans_num):
    """
    /question/id/ans_num
    Gets the next question based on the ans_num
    """
    if request.method == 'GET':
        question = Question.objects.get(id=id)
        answer = Answer.objects.get(question=question, answer_number=ans_num)
        next_question = answer.next_question
        serializer = QuestionSerializer(next_question, many=False)
        return Response(serializer.data)

class HighlightTasks(GenericAPIView):
    # GenericAPIView assists by providing the pagination settings
    # and helpful pagination API

    """
    /highlighter_tasks2

    Provides highlight tasks as an array of objects, where each object has
    all the information to set up the highlight_tool for a task:

    1. the project description
    2. the topics to use
    3. the article to highlight

    This endpoint is paginated for use without Pybossa in the loop.
    """
    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):

        # Pagination code is derived from rest_framework.mixins.ListModelMixin
        # and rest_framework.generics.GenericAPIView:get_serializer
        project = Project.objects.get(name="Deciding Force")
        topics = Topic.objects.filter(parent=None)

        articles = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(articles)
        if page is not None:
            tasks = self.collectTaskList(page, project, topics)
            return self.get_paginated_response(tasks)

        tasks = self.collectTaskList(articles, project, topics)
        return Response(tasks)

    def collectTaskList(self, articles, project, topics):
        # next line processes features like ?format=json
        kwargs = {'context': self.get_serializer_context()}

        project_data = ProjectSerializer(project, many=False, **kwargs).data
        topics_data = RootTopicSerializer(topics, many=True, **kwargs).data
        return [{ "project": project_data,
                  "topics": topics_data,
                  "article":
                      ArticleSerializer(article, many=False, **kwargs).data
               } for article in articles ]


class HighlightTasksNoPage(HighlightTasks):
    """
    /highlighter_tasks

    Provides highlight tasks as an array of objects, where each object has
    all the information to set up the highlight_tool for a task:

    1. the project description
    2. the topics to use
    3. the article to highlight

    This endpoint is **not paginated**, as it will be used for bulk export
    to Pybossa.
    """

    pagination_class = None

# This shows how to do additional filtering if needed...
#    def get_queryset(self):
#        articles = super(HighlightTasksNoPage, self).get_queryset()
#        return articles.filter(
#            id__in=[9, 11, 38, 53, 55, 202, 209, 236, 259]
#        ).order_by('id')


@api_view(['GET'])
def quiz_tasks(request):
    """
    /quiz_tasks

    Provides tasks as an array of objects, where each object has
    all the information to set up the quiz for a task:

    1. the project description
    2. the Topic
    3. the article
    4. the highlights for the Topic, per article
    5. the questions and answers for this Topic
    """
    if request.method == 'GET':
        taskList = []
        project = Project.objects.get(name__exact="Deciding Force")

        # Researcher interface will allow selecting topic.
        topic = Topic.objects.get(name__exact="Protester")

# WIP: getting all subtopics
#       topictree = Topic.objects.raw("""
#           WITH RECURSIVE subtopic(id, parent_id, name) AS (
#               SELECT id, parent_id, name FROM thresher_topic WHERE id=%s
#             UNION ALL
#               SELECT t.id, t.parent_id, t.name
#               FROM subtopic, thresher_topic t
#               WHERE t.parent_id = subtopic.id
#           )
#           SELECT id, parent_id
#           FROM subtopic LIMIT 100;
#       """, [topic.id])

        # replace this with recursive query above to find all
        # children of Protester, not just hard coded "Event type"
        topictree = (Topic.objects.filter(name__exact="Event type")
                     .prefetch_related("questions__answers"))
        questions = [ q for t in topictree for q in t.questions.all() ]

        # Set up Prefetch that will cache just the highlights matching
        # this topic to article.users_highlights[n].highlightsForTopic
        # This approach uses only 3 SQL queries, instead of hitting the
        # database once or twice for every article looped over.
        topicHighlights = (HighlightGroup.objects.filter(topic=topic)
                           .order_by("case_number"))
        fetchHighlights = Prefetch("users_highlights__highlights",
                                   queryset=topicHighlights,
                                   to_attr="highlightsForTopic")
        # Currently selecting all articles highlighted with the topic
        # Researcher interface will allow selecting subset of those articles
        # We will also need ability to designate canonical approved highlights
        # for a given article.
        articles = (Article.objects
                    .filter(users_highlights__highlights__topic=topic)
                    .prefetch_related(fetchHighlights))
        # Limit to 10 for development. Export all for production.
        articles = articles.order_by("id")[:10]

        for article in articles:
            # Our prefetched highlightsForTopic is nested under
            # the ArticleHightlight record, in HighlightGroup
            # Not expecting more than one ArticleHighlight record
            # but safest to code as if there could be more than one.
            highlights = [ hg
                           for ah in article.users_highlights.all()
                           for hg in ah.highlightsForTopic
                         ]

            taskList.append({
               "project": ProjectSerializer(project, many=False).data,
               "topic": TopicSerializer(topic, many=False).data,
               "topictree": TopicSerializer(topictree, many=True).data,
               "article": ArticleSerializer(article, many=False).data,
               # Get prefetch field "article.highlightsForTopic" to work
               "highlights": HighlightGroupSerializer(
                                 highlights, many=True).data,
               "questions": QuestionSerializer(questions, many=True).data
            })

        return Response(taskList)

# Register our viewsets with the router
ROUTER = routers.DefaultRouter()
ROUTER.register(r'projects', ProjectViewSet)
ROUTER.register(r'users', UserProfileViewSet)
ROUTER.register(r'articles', ArticleViewSet)
ROUTER.register(r'topics', TopicViewSet)
ROUTER.register(r'highlight_groups', HighlightGroupViewSet)
ROUTER.register(r'article_highlights', ArticleHighlightViewSet)
