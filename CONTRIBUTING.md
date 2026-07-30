# Contributing

Thanks for helping improve the Environmental Intelligence Dashboard. By participating, you agree to follow the [Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Development setup

1. Fork the repository and create a branch from `main`.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and set local values as needed.
5. Run `python manage.py check` and `python manage.py test` before opening a pull request.

## Pull requests

Describe the change, explain how it was tested, and link any related issue. Do not commit credentials, generated caches, local databases, large derivative datasets, or changes to trained model artifacts unless the pull request explicitly concerns the model.

## Code standards

Follow existing Django and Python conventions, keep changes scoped, and add or update tests when behavior changes. Do not modify migrations, database schema, or the AI prediction module as part of unrelated work.
