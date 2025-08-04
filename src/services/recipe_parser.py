from recipe_scrapers import scrape_html
from models.ingredient import Ingredient
from models.recipe import Recipe


class RecipeParser:
    """
    Utility class for parsing recipes from HTML with the recipe-scrapers library.

    Parameters:
        url (str): The url where the HTML content came from
        html (str): The HTML content to parse
    """

    _url: str
    _html: str
    _title: str
    _minutes: int
    _servings: int
    _ingredients: list[str]
    _directions: list[str]
    _user_agent: str

    def __init__(self, url: str, html: str) -> None:
        self._url = url
        self._html = html

    def parse(self):
        """
        Parses the recipe. Data is stored internally and can be fetched with get_as_recipe().
        """
        scraper = scrape_html(self._html, org_url=self._url)
        self._title = scraper.title()
        self._minutes = scraper.total_time()
        servings = scraper.yields()  # type: ignore
        self._servings = servings.split(" ")[0]  # type: ignore
        self._ingredients = scraper.ingredients()
        self._directions = scraper.instructions_list()

    def get_as_recipe(self):
        """
        Returns the scraped recipe (if it exists) as a Recipe model instance.

        Returns:
            Recipe: The scraped recipe
        """
        return Recipe(
            title=self._title,
            servings=int(self._servings),
            minutes=int(self._minutes),
            ingredients=[Ingredient.from_string(ing) for ing in self._ingredients],
            directions=self._directions,
            source_url=self._url,
        )
