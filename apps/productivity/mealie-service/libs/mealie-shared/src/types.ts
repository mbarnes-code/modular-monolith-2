// Shared types and interfaces for Mealie
export interface Recipe {
  id?: string;
  name: string;
  description?: string;
  recipeIngredients: RecipeIngredient[];
  recipeInstructions: RecipeInstruction[];
  tags?: RecipeTag[];
  dateAdded?: Date;
  dateUpdated?: Date;
  image?: string;
}

export interface RecipeIngredient {
  title?: string;
  note?: string;
  unit?: Unit;
  food?: Food;
  quantity?: number;
}

export interface RecipeInstruction {
  title?: string;
  text: string;
  ingredientReferences?: IngredientReference[];
}

export interface RecipeTag {
  id?: string;
  name: string;
  slug: string;
}

export interface Unit {
  id?: string;
  name: string;
  abbreviation?: string;
  plural_name?: string;
}

export interface Food {
  id?: string;
  name: string;
  description?: string;
  plural_name?: string;
}

export interface IngredientReference {
  referenceId?: string;
}

// API Response types
export interface ApiResponse<T> {
  items?: T[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface MealieUser {
  id?: string;
  username: string;
  email: string;
  full_name?: string;
  admin: boolean;
  group: string;
}

export interface MealPlan {
  id?: string;
  date: Date;
  entry_type: string;
  title?: string;
  text?: string;
  recipe?: Recipe;
}

// Configuration types
export interface MealieConfig {
  port: number;
  host: string;
  database: {
    url: string;
    type: string;
  };
  frontend: {
    enabled: boolean;
    path: string;
    api_url: string;
  };
}

// Backend configuration
export interface MealieBackendConfig {
  database_url: string;
  secret_key: string;
  host: string;
  port: number;
  workers: number;
  log_level: string;
}