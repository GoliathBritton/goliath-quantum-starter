from typing import Dict, Any

def run_recipe(recipe: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    return {"status":"ok","actions_executed": len(recipe.get("actions", []))}
