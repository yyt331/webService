import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .models import Story, Author
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.dateformat import DateFormat

# Create your views here.

@csrf_exempt
@require_POST
def log_in(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponse('Logged in successfully. Welcome!', status=200)
    else:
        return HttpResponse('Error, invalid credentials', status=400)

@csrf_exempt
@require_POST
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse('Logged out successfully. Have a nice day!', status=200, content_type='text/plain')
    else:
        return HttpResponse('Logged out failed. No user is logged in.', status=400, content_type='text/plain')

@csrf_exempt
def stories(request):
    # Function to post stories with POST request
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Error, authentication required.', status=503)

        try:
            data = json.loads(request.body)
            
            new_story = Story(
                headline=data['headline'],
                category=data['category'],
                region=data['region'],
                details=data['details'],
                author=Author.objects.get(user=request.user)
            )

            # Check if story data violates the model constraints
            new_story.full_clean()

            new_story.save()
            
            return JsonResponse({'message': 'Story posted successfully.'}, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e.messages)}, status=503)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=503)

    # Function to get stories with GET request
    elif request.method == 'GET':
        category = request.GET.get('category', '')
        region = request.GET.get('region', '')
        date_str = request.GET.get('date', '')
        
        stories_query = Story.objects.all()

        if category and category != '*':
            stories_query = stories_query.filter(category=category)
        
        if region and region != '*':
            stories_query = stories_query.filter(region=region)
        
        if date_str and date_str != '*':
            try:
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                stories_query = stories_query.filter(date__gte=date_obj)
            except ValueError:
                return HttpResponse('Invalid date format. Use dd/mm/yyyy.', status=404, content_type='text/plain')
        
    if stories_query.exists():
        stories_list = [
            {
                'key': story.pk,
                'headline': story.headline,
                'story_cat': story.category,
                'story_region': story.region,
                'author': story.author.user.username,
                'story_date': DateFormat(story.date).format('d/m/Y'),
                'story_details': story.details
            } for story in stories_query
        ]
        return JsonResponse({'stories': stories_list}, status=200)
    else:
        return HttpResponse('No stories found.', status=404, content_type='text/plain')

@csrf_exempt
def delete_story(request, story_key):
    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return HttpResponse('Authentication required', status=503)
        
        try:
            story = Story.objects.get(pk=story_key)
            story.delete()
            return HttpResponse('Story deleted successfully', status=200)
        except Story.DoesNotExist:
            return HttpResponse('Story not found', status=503)
        except Exception as e:
            return HttpResponse('Error deleting story. Please try again', status=503)