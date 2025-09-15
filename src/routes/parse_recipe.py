from fastapi import APIRouter
from models.recipe import Recipe
from services.recipe_parser import RecipeParser
from urllib.parse import unquote
from pydantic import BaseModel
from fastapi_simple_rate_limiter import rate_limiter  # type: ignore

router = APIRouter()


class ParseRecipeRequest(BaseModel):
    url: str
    html: str


@router.post("/parse-recipe")
@rate_limiter(limit=5, seconds=60)
async def parse_recipe(body: ParseRecipeRequest) -> Recipe:
    parser = RecipeParser(unquote(body.url), unquote(body.html))
    parser.parse()
    return parser.get_as_recipe()
