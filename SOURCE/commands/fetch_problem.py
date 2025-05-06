import click
import requests
import random
from SOURCE.modules.cfp_problem import Problem

@click.command()
@click.option('--rating', type=int, help='Rating of the problem to fetch.')
@click.option('--min-rating', type=int, help='Minimum rating for random problem.')
@click.option('--max-rating', type=int, help='Maximum rating for random problem.')
def fetch_problem(rating, min_rating, max_rating):
    """
    Fetch a random Codeforces problem by exact rating or within a rating range.
    """
    try:
        resp = requests.get("https://codeforces.com/api/problemset.problems")
        data = resp.json()

        if data['status'] != 'OK':
            print('API error:', data.get('comment', 'Unknown error'))
            return

        problems = data['result']['problems']

        # Filter by exact rating
        if rating:
            filtered_problems = [p for p in problems if p.get('rating') == rating]
        # Filter by rating range
        elif min_rating is not None and max_rating is not None:
            filtered_problems = [p for p in problems if p.get('rating') and min_rating <= p['rating'] <= max_rating]
        else:
            print("Please provide either --rating or both --min-rating and --max-rating.")
            return

        if not filtered_problems:
            print("No problems found for the given rating criteria.")
            return

        problem_data = random.choice(filtered_problems)
        problem = Problem.from_dict(problem_data)

        print(f"🔹 Contest ID: {problem.contest_id}")
        print(f"🔹 Index: {problem.index}")
        print(f"🔹 Name: {problem.name}")
        print(f"🔹 Rating: {problem.rating}")
        print(f"🔹 Tags: {', '.join(problem.tags)}")
        print(f"🔹 URL: https://codeforces.com/contest/{problem.contest_id}/problem/{problem.index}")

    except Exception as e:
        print("Error fetching the problem data:", e)
