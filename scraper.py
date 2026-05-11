from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from google_play_scraper import search
from rapidfuzz import fuzz

from distraction_levels import get_category, get_category_distraction, CATEGORY_DISTRACTION_VALUES
from types_lib.constants import *
from types_lib.scraper_types import ScraperInputType, ScraperResponse

UNKNOWN_CATEGORY = "Utility"
UNKNOWN_DISTRACTION = CATEGORY_DISTRACTION_VALUES[UNKNOWN_CATEGORY]

def is_valid_match(input_name: str, found_name: str, threshold: int = 60) -> bool:
    """
    Checks how close an app is to actually being what is found, used due to there being apps
    not in app store and then they just give trash found names
    :param input_name: app name we found on the phone and are looking for
    :param found_name: name found in actuall app store
    :param threshold: accurassy
    :return: if its actually on the app store or not
    """
    return fuzz.token_set_ratio(input_name.lower(), found_name.lower()) >= threshold

def fetch_app(app_name: str) -> ScraperResponse:
    try:
        app_name = str(app_name)

        search_results = search(app_name, n_hits=5)

        if not search_results:
            return ScraperResponse(
                app=app_name,
                category=UNKNOWN_CATEGORY,
                distraction_value=UNKNOWN_DISTRACTION,
            )

        best_match = None #best match for an app from the 5 search finds

        for app in search_results:
            title = app.get(TITLE)
            if is_valid_match(app_name, title):
                best_match = app
                break

        if not best_match:
            return ScraperResponse(
                app=app_name,
                category=UNKNOWN_CATEGORY,
                distraction_value=UNKNOWN_DISTRACTION,
            )

        genre = best_match.get(GENRE)
        category = get_category(genre)
        distraction_value = get_category_distraction(genre)

        if category == UNKNOWN:
            category = UNKNOWN_CATEGORY
            distraction_value = UNKNOWN_DISTRACTION

        return ScraperResponse(
            app=app_name,
            category=category,
            distraction_value=distraction_value,
        )

    except Exception:
        return ScraperResponse(app=app_name)


def get_app_genres(app_names: ScraperInputType) -> List[ScraperResponse]:
    results: List[ScraperResponse] = []

    apps = app_names.apps
    max_threads = min(20, len(apps))  # safe limit, can increase but can risk 429

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_app = {
            executor.submit(fetch_app, app): app for app in apps
        }

        for future in as_completed(future_to_app):
            results.append(future.result())

    return results