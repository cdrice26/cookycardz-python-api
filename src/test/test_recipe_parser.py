import pytest
from unittest.mock import patch, MagicMock
from services.recipe_parser import RecipeParser
from models.recipe import Recipe


class TestRecipeParser:

    @pytest.fixture
    def parser(self) -> RecipeParser:
        return RecipeParser("http://example.com/recipe", "<html></html>")

    @patch("services.recipe_parser.scrape_html")
    def test_parse_success(
        self,
        mock_scrape_html: MagicMock,
        parser: RecipeParser,
    ) -> None:

        # Mocking the scrape_html function
        mock_parser_instance: MagicMock = MagicMock()
        mock_parser_instance.title.return_value = "Test Recipe"
        mock_parser_instance.total_time.return_value = 30
        mock_parser_instance.yields.return_value = "4 servings"
        mock_parser_instance.ingredients.return_value = ["1 cup of flour", "2 eggs"]
        mock_parser_instance.instructions_list.return_value = [
            "Mix ingredients",
            "Bake at 350 degrees",
        ]
        mock_scrape_html.return_value = mock_parser_instance

        # Call the method
        parser.parse()

        # Assertions
        assert parser._title == "Test Recipe"  # type: ignore
        assert parser._minutes == 30  # type: ignore
        assert parser._servings == "4"  # type: ignore
        assert parser._ingredients == ["1 cup of flour", "2 eggs"]  # type: ignore
        assert parser._directions == ["Mix ingredients", "Bake at 350 degrees"]  # type: ignore

    @patch("services.recipe_parser.scrape_html")
    def test_get_as_recipe(
        self,
        mock_scrape_html: MagicMock,
        parser: RecipeParser,
    ) -> None:

        # Mocking the scrape_html function
        mock_parser_instance: MagicMock = MagicMock()
        mock_parser_instance.title.return_value = "Test Recipe"
        mock_parser_instance.total_time.return_value = 30
        mock_parser_instance.yields.return_value = "4 servings"
        mock_parser_instance.ingredients.return_value = ["1 cup flour", "2 eggs"]
        mock_parser_instance.instructions_list.return_value = [
            "Mix ingredients",
            "Bake at 350 degrees",
        ]
        mock_scrape_html.return_value = mock_parser_instance

        # Call the method to scrape
        parser.parse()

        # Get the recipe
        recipe: Recipe = parser.get_as_recipe()

        # Assertions
        assert isinstance(recipe, Recipe)
        assert recipe.title == "Test Recipe"
        assert recipe.servings == 4
        assert recipe.minutes == 30
        assert len(recipe.ingredients) == 2
        assert recipe.ingredients[0].name == "flour"
        assert recipe.ingredients[0].unit == "cup"
        assert recipe.ingredients[0].amount == 1.0
        assert recipe.ingredients[1].name == "eggs"
        assert recipe.ingredients[1].amount == 2.0
        assert recipe.ingredients[1].unit == "count"
        assert recipe.directions == ["Mix ingredients", "Bake at 350 degrees"]
        assert recipe.source_url == "http://example.com/recipe"
