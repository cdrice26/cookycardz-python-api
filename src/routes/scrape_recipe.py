from fastapi import APIRouter, Query
from models.recipe import Recipe
from services.recipe_parser import RecipeParser
from urllib.parse import unquote
from typing import Annotated
from fastapi_simple_rate_limiter import rate_limiter  # type: ignore

router = APIRouter()


@router.get("/scrape-recipe")
@rate_limiter(limit=5, seconds=60)
async def scrape_recipe(
    url: Annotated[str, Query()], html: Annotated[str, Query()]
) -> Recipe:
    parser = RecipeParser(unquote(url), unquote(html))
    parser.parse()
    return parser.get_as_recipe()
