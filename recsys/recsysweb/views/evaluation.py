# django
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.conf                    import settings
import logging


# Domain
from ..domain                       import DomainContext


ctx = DomainContext()


@login_required
def likes(request):
    request = RequestHelper(request)

    if request.is_post:
        ctx.item_service.score_items_by(
            request.user,
            items_rating = request.items_rating
        )
        ctx.evaluation_service.evaluate_session(request.user, request.items_rating)

    recommendations = ctx.recommender_service \
        .find_recommendations_from_active_evaluation(request.user)

    response = build_response(recommendations, request.user)

    return render(request.request, 'single/likes.html', response)


def build_response(recommendations, user):
    metric = ctx.evaluation_service.find_metric_by_active_and_user(user)

    response = {
        'score_levels' : settings.SCORE_LEVELS,
        'no_image_url' : settings.NO_IMAGE_ITEM_URL,
        'metric'       : metric
    }

    if recommendations.empty:
        response['messages'] = [recommendations.info, 'Please be patient while we calculate the new recommendations. This process can take between 5 and 10 minutes depending on the load and the amount of users.']
    else:
        recommendations.items = recommendations.items[: recommendations.metadata.n_items_by_session]
        response['recommendations']     = recommendations
        response['user_n_interactions'] = ctx.interaction_service.count_by_user(user)

    return response


class RequestHelper:
    def __init__(self, request): self.request = request

    @property
    def items_rating(self):
        return {int(key):int(value) for key, value in self.request.POST.items() if key not in ['csrfmiddlewaretoken']}

    @property
    def user(self): return self.request.user

    @property
    def is_post(self): return self.request.method == "POST"
